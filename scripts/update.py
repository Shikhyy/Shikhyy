#!/usr/bin/env python3
"""Refresh live GitHub data, regenerate the graphics and rewrite the dynamic README blocks.

Runs locally (needs the gh CLI signed in) and in the scheduled GitHub Action, which supplies
GH_TOKEN. Only the Python standard library is used.

README blocks between <!--AUTO:name:start--> and <!--AUTO:name:end--> are owned by this script.
"""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from projects import LABELS, SPOTLIGHT  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
USER = "Shikhyy"

MAX_LOGOS = 6


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def graphql(query):
    return json.loads(gh("api", "graphql", "-f", "query=" + query))["data"]


def save(name, obj, compact=False):
    DATA.mkdir(exist_ok=True)
    text = json.dumps(obj, separators=(",", ":")) if compact else json.dumps(obj, indent=1)
    (DATA / name).write_text(text + "\n")


def label(owner):
    return LABELS.get(owner, owner)


def fmt(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f"{d.strftime('%b')} {d.day}"


def join_names(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def esc(title):
    return title.replace("[", "\\[").replace("]", "\\]")


# ------------------------------------------------------------------ fetch
def fetch_calendar():
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions '
         'weeks{contributionDays{date contributionCount weekday}}}}}}') % USER
    save("calendar.json", graphql(q)["user"]["contributionsCollection"]["contributionCalendar"], compact=True)


def fetch_stats():
    q = ('{user(login:"%s"){createdAt followers{totalCount} '
         'repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false){totalCount nodes{stargazerCount forkCount}} '
         'pullRequests{totalCount} mergedPRs: pullRequests(states:MERGED){totalCount} issues{totalCount} '
         'contributionsCollection{totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions '
         'totalRepositoriesWithContributedCommits} '
         'repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST],includeUserRepositories:false){totalCount}}}') % USER
    u = graphql(q)["user"]
    cc = u["contributionsCollection"]
    stats = {
        "createdAt": u["createdAt"], "followers": u["followers"]["totalCount"],
        "pubRepos": u["repositories"]["totalCount"] - 1,          # the profile repo itself is not a project
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "forks": sum(n["forkCount"] for n in u["repositories"]["nodes"]),
        "prs": u["pullRequests"]["totalCount"], "merged": u["mergedPRs"]["totalCount"], "issues": u["issues"]["totalCount"],
        "commits": cc["totalCommitContributions"], "prContrib": cc["totalPullRequestContributions"],
        "reviews": cc["totalPullRequestReviewContributions"], "reposCommitted": cc["totalRepositoriesWithContributedCommits"],
        "contributedTo": u["repositoriesContributedTo"]["totalCount"],
    }
    save("stats.json", stats)
    return stats


def fetch_repos():
    q = ('{user(login:"%s"){repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{'
         'name pushedAt diskUsage primaryLanguage{name} languages(first:3,orderBy:{field:SIZE,direction:DESC}){nodes{name}}}}}}') % USER
    nodes = graphql(q)["user"]["repositories"]["nodes"]
    repos = [{"name": n["name"], "pushed": n["pushedAt"], "lang": (n["primaryLanguage"] or {}).get("name"),
              "langs": [l["name"] for l in n["languages"]["nodes"]]} for n in nodes if n["name"] != USER and n["diskUsage"] > 0]   # skip the profile repo and empty repos
    save("repos_live.json", repos)
    return repos


def fetch_oss():
    """Open and merged pull requests to repositories owned by organisations other than me."""
    rows = json.loads(gh("search", "prs", "--author", USER, "--limit", "100", "--json",
                         "repository,title,state,url,createdAt,closedAt,updatedAt"))
    owner_type, out = {}, []
    for r in rows:
        owner, repo = r["repository"]["nameWithOwner"].split("/")
        if owner.lower() == USER.lower() or r["state"] not in ("merged", "open"):
            continue
        if owner not in owner_type:
            owner_type[owner] = gh("api", f"users/{owner}", "--jq", ".type").strip()
        if owner_type[owner] != "Organization":
            continue
        when = r["closedAt"] if (r["state"] == "merged" and r.get("closedAt")) else r["createdAt"]
        out.append({"owner": owner, "repo": repo, "title": r["title"], "url": r["url"], "state": r["state"], "date": when[:10]})
    out.sort(key=lambda p: (p["date"], p["url"]), reverse=True)
    save("oss.json", out)
    return out


def fetch_week():
    """Commits, repositories and pull requests over the last seven days."""
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    start = now - datetime.timedelta(days=7)
    iso = lambda d: d.isoformat().replace("+00:00", "Z")
    q = ('{user(login:"%s"){contributionsCollection(from:"%s",to:"%s"){totalCommitContributions totalPullRequestContributions '
         'totalRepositoriesWithContributedCommits commitContributionsByRepository(maxRepositories:10){repository{nameWithOwner} '
         'contributions{totalCount}}}}}') % (USER, iso(start), iso(now))
    cc = graphql(q)["user"]["contributionsCollection"]
    top = sorted(((x["repository"]["nameWithOwner"], x["contributions"]["totalCount"]) for x in cc["commitContributionsByRepository"]),
                 key=lambda t: -t[1])
    wk = {"commits": cc["totalCommitContributions"], "prs": cc["totalPullRequestContributions"],
          "repos": cc["totalRepositoriesWithContributedCommits"], "top": top[:5]}
    save("week.json", wk)
    return wk


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def week_text(wk):
    if not wk["commits"] and not wk["prs"]:
        return "a quiet one so far."
    text = f"{plural(wk['commits'], 'commit')} across {plural(wk['repos'], 'repository').replace('repositorys', 'repositories')} and {plural(wk['prs'], 'pull request')}"
    # skip the profile repo itself (those commits are just me editing this page) and drop my own prefix
    top = [f"**{name.replace(USER + '/', '')}** ({n})" for name, n in wk["top"] if n and name != f"{USER}/{USER}"][:3]
    return text + (f", mostly in {join_names(top)}." if top else ".")


def spotlight_block():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    name, repo, fact = SPOTLIGHT[today.toordinal() % len(SPOTLIGHT)]
    return f"\n> **Project spotlight, changes daily:** [{name}](https://github.com/{USER}/{repo})\n> {fact}\n\n"


# ------------------------------------------------------------------ README blocks
def build_blocks(stats, repos, oss, week):
    merged = [p for p in oss if p["state"] == "merged"]
    by_owner = {}
    for p in oss:
        by_owner.setdefault(p["owner"], []).append(p)
    owners = sorted(by_owner, key=lambda o: max(p["date"] for p in by_owner[o]), reverse=True)

    # numbers used in the About text and table
    commits_floor = stats["commits"] // 100 * 100
    about = f"over {commits_floor:,} commits and {len(repos)} original repositories"
    merged_owners = sorted({p["owner"] for p in merged}, key=lambda o: (-sum(1 for p in merged if p["owner"] == o), o))   # ties broken by name so reruns are identical
    row = f"{len(merged)} merged pull requests across {join_names([label(o) for o in merged_owners])}"

    # logo row, most recently active project first
    shown = owners[:MAX_LOGOS]
    width = 100 // max(1, len(shown))
    cells = []
    for o in shown:
        ps = by_owner[o]
        m = sum(1 for p in ps if p["state"] == "merged")
        op = len(ps) - m
        sub = ", ".join(x for x in (f"{m} merged" if m else "", f"{op} open" if op else "") if x)
        cells.append(
            f'    <td align="center" width="{width}%">\n'
            f'      <a href="https://github.com/{o}/{ps[0]["repo"]}/pulls?q=is%3Apr+author%3A{USER}">'
            f'<img src="https://github.com/{o}.png?size=160" width="56" height="56" alt="{label(o)}"></a><br>\n'
            f'      <b>{label(o)}</b><br>\n      <sub>{sub}</sub>\n    </td>')
    logos = '\n<div align="center">\n<table>\n  <tr>\n' + "\n".join(cells) + "\n  </tr>\n</table>\n</div>\n"

    # latest activity plus the full list
    latest = ["", "**Latest activity**", ""]
    for p in oss[:6]:
        status = f"**Merged** {fmt(p['date'])}" if p["state"] == "merged" else f"**Open** since {fmt(p['date'])}"
        latest.append(f"- {status}: [{esc(p['title'])}]({p['url']}) ({label(p['owner'])})")
    groups = []
    for o in owners:
        ps = by_owner[o]
        multi = len({p["repo"] for p in ps}) > 1
        groups.append(f"**{label(o)}**")
        for p in ps:
            note = ("merged " if p["state"] == "merged" else "open since ") + fmt(p["date"])
            if multi:
                note = f"{p['repo']}, {note}"
            groups.append(f"- [{esc(p['title'])}]({p['url']}) ({note})")
        groups.append("")
    details = ("\n<details>\n<summary>All pull requests by project (" + str(len(oss)) + ")</summary>\n<br>\n\n"
               + "\n".join(groups) + "\n</details>\n")
    return {"this_week": week_text(week), "spotlight": spotlight_block(), "about_numbers": about, "oss_row": row, "oss_logos": logos, "oss_prs": "\n".join(latest) + "\n" + details}


def fill(readme, name, content):
    pat = re.compile(rf"(<!--AUTO:{name}:start-->)(.*?)(<!--AUTO:{name}:end-->)", re.S)
    if not pat.search(readme):
        raise SystemExit(f"README marker '{name}' not found")
    return pat.sub(lambda m: m.group(1) + content + m.group(3), readme, count=1)


def snapshot():
    out = {}
    for sub in ("data", "assets", "web"):
        for f in sorted((ROOT / sub).rglob("*")):
            if f.is_file():
                out[str(f.relative_to(ROOT))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def main():
    before = snapshot()
    fetch_calendar()
    repos = fetch_repos()
    stats = fetch_stats()
    stats["pubRepos"] = len(repos)          # one source of truth for the repository count
    save("stats.json", stats)
    oss = fetch_oss()
    week = fetch_week()
    subprocess.check_call([sys.executable, str(ROOT / "scripts/generate.py")], stdout=subprocess.DEVNULL)

    readme_path = ROOT / "README.md"
    old = readme_path.read_text()
    new = old
    for name, content in build_blocks(stats, repos, oss, week).items():
        new = fill(new, name, content)
    changed = new != old or snapshot() != before
    if changed:
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        new = fill(new, "updated", f"Last updated {today} UTC")
    if new != old:
        readme_path.write_text(new)
    print("changed" if changed else "no changes",
          f"| commits {stats['commits']} | repos {len(repos)} | oss prs {len(oss)} "
          f"({sum(1 for p in oss if p['state'] == 'merged')} merged)")


if __name__ == "__main__":
    main()
