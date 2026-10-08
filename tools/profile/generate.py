#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import xml.sax.saxutils as saxutils

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "assets"
WRITING_DIR = ASSETS_DIR / "writing"
LINKS_DIR = ASSETS_DIR / "links"
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

ALL_PROJECT_NAMES = [
    "accomplish", "AEOspy", "Agentarena", "AgentWill", "AgriSupply", "AI_Parliament", "Apex", "BidWire",
    "cairnquill", "Cards-Against-Humanity", "Contenthub", "Credo", "Decoding-Customer-Value",
    "Delhivery-Graph-Intelligence-System", "Dotsafe", "EcoTrack", "firstlight", "GOSSIP",
    "hiver-sde-assignment", "LoyaltyChain", "Nexus", "NovaStream", "Pantheon", "Petal", "PlayStake",
    "precedent", "Pulse", "pulsetwin", "ResilientPay", "resilientpay-android", "resilientpay-web",
    "squadrune", "stratify", "TSA-Capstone", "VaultGate", "Vision-Quest", "VitaSync", "VolunteerIQ",
    "WakeTogether", "wyrmline", "YoSubs"
]

FEATURED_PROJECTS = [
    "wyrmline", "Nexus", "EcoTrack", "ResilientPay", "accomplish",
    "AEOspy", "AI_Parliament", "Agentarena", "VitaSync", "Delhivery-Graph-Intelligence-System"
]

STACK = {
    "Languages": ["TypeScript", "JavaScript", "Python", "Rust", "Kotlin", "Solidity"],
    "Frameworks / Tools": ["React", "Next.js", "Node.js", "FastAPI", "Tailwind CSS", "Docker"],
    "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite"],
    "Cloud / Platforms": ["GitHub Actions", "AWS", "Vercel", "Android", "Linux"]
}


@dataclass
class Project:
    name: str
    url: str
    description: str
    stars: int = 0
    language: str | None = None


@dataclass
class Article:
    title: str
    url: str
    published_at: str
    reactions: int
    comments: int


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dirs() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    WRITING_DIR.mkdir(parents=True, exist_ok=True)
    LINKS_DIR.mkdir(parents=True, exist_ok=True)


def fetch_json(url: str, token: str | None = None, timeout: int = 20) -> Any:
    headers = {
        "Accept": "application/json",
        "User-Agent": "Shikhyy-profile-generator"
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def graphql(query: str, variables: dict[str, Any], token: str | None) -> Any:
    if not token:
        return None
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "User-Agent": "Shikhyy-profile-generator"
    }
    req = Request("https://api.github.com/graphql", data=body, method="POST", headers=headers)
    try:
        with urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if payload.get("errors"):
                return None
            return payload.get("data")
    except (HTTPError, URLError, TimeoutError):
        return None


def fallback_contributions(today: date | None = None, days: int = 365) -> list[dict[str, Any]]:
    today = today or date.today()
    out = []
    for index in range(days):
        current = today - timedelta(days=(days - 1 - index))
        seed = current.toordinal()
        level = (seed * 1103515245 + 12345) % 11
        count = 0 if level < 4 else (level - 3)
        out.append({"date": current.isoformat(), "count": int(count)})
    return out


def normalize_contributions(days_payload: Any, today: date | None = None) -> list[dict[str, Any]]:
    today = today or date.today()
    if not isinstance(days_payload, list):
        return fallback_contributions(today=today)
    normalized: list[dict[str, Any]] = []
    for item in days_payload:
        if not isinstance(item, dict):
            continue
        raw_date = item.get("date")
        raw_count = item.get("contributionCount", item.get("count", 0))
        try:
            parsed = date.fromisoformat(str(raw_date))
            count = max(0, int(raw_count))
            normalized.append({"date": parsed.isoformat(), "count": count})
        except (TypeError, ValueError):
            continue
    if len(normalized) < 200:
        return fallback_contributions(today=today)
    normalized.sort(key=lambda x: x["date"])
    return normalized[-365:]


def calculate_streaks(days: list[dict[str, Any]]) -> tuple[int, int]:
    current = 0
    longest = 0
    run = 0
    for day in days:
        if day["count"] > 0:
            run += 1
        else:
            longest = max(longest, run)
            run = 0
    longest = max(longest, run)
    for day in reversed(days):
        if day["count"] > 0:
            current += 1
        else:
            break
    return current, longest


def summarize_languages(projects: list[Project]) -> list[str]:
    counts: dict[str, int] = {}
    for project in projects:
        if project.language:
            counts[project.language] = counts.get(project.language, 0) + 1
    sorted_langs = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return [lang for lang, _ in sorted_langs[:5]]


def collect_repo_data(username: str, token: str | None) -> list[Project]:
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    try:
        repos = fetch_json(url, token=token)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        repos = []

    by_name: dict[str, Project] = {}
    if isinstance(repos, list):
        for repo in repos:
            name = repo.get("name")
            if not isinstance(name, str):
                continue
            desc = repo.get("description")
            description = desc.strip() if isinstance(desc, str) and desc.strip() else "Description not provided in repository metadata."
            by_name[name.lower()] = Project(
                name=name,
                url=repo.get("html_url", f"https://github.com/{username}/{name}"),
                description=description,
                stars=int(repo.get("stargazers_count", 0) or 0),
                language=repo.get("language")
            )

    projects: list[Project] = []
    for repo_name in ALL_PROJECT_NAMES:
        key = repo_name.lower()
        if key in by_name:
            projects.append(by_name[key])
            continue
        projects.append(Project(
            name=repo_name,
            url=f"https://github.com/{username}/{repo_name}",
            description="Description not provided in repository metadata.",
            stars=0,
            language=None
        ))
    return projects


def collect_github_stats(username: str, token: str | None) -> dict[str, Any]:
    today = date.today()
    fallback_days = fallback_contributions(today=today)

    graph_query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        followers { totalCount }
        pullRequests { totalCount }
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    from_dt = datetime.combine(today - timedelta(days=364), datetime.min.time(), tzinfo=timezone.utc).isoformat()
    to_dt = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc).isoformat()

    graph_data = graphql(graph_query, {"login": username, "from": from_dt, "to": to_dt}, token=token)

    contributions = fallback_days
    followers = 0
    prs = 0
    contribution_total = sum(day["count"] for day in contributions)
    contribution_source = "Fallback generated sample used because live GitHub contribution data was unavailable."

    if graph_data and graph_data.get("user"):
        user = graph_data["user"]
        followers = int(user.get("followers", {}).get("totalCount", 0) or 0)
        prs = int(user.get("pullRequests", {}).get("totalCount", 0) or 0)

        weeks = user.get("contributionsCollection", {}).get("contributionCalendar", {}).get("weeks", [])
        raw_days = []
        for week in weeks:
            raw_days.extend(week.get("contributionDays", []))
        contributions = normalize_contributions(raw_days, today=today)
        contribution_total = int(user.get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", 0) or 0)
        contribution_source = "Live GitHub contribution calendar (GraphQL)."

    return {
        "followers": followers,
        "pull_requests": prs,
        "contributions_last_year": contribution_total,
        "contribution_days": contributions,
        "contribution_source": contribution_source,
    }


def collect_dev_data(dev_username: str, enabled: bool) -> dict[str, Any] | None:
    if not enabled or not dev_username.strip():
        return None
    try:
        profile = fetch_json(f"https://dev.to/api/users/by_username?url={dev_username.strip()}")
        articles_payload = fetch_json(f"https://dev.to/api/articles?username={dev_username.strip()}&per_page=5")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None

    articles: list[Article] = []
    reactions = 0
    comments = 0
    for item in articles_payload if isinstance(articles_payload, list) else []:
        article = Article(
            title=item.get("title", "Untitled"),
            url=item.get("url", "https://dev.to"),
            published_at=item.get("published_at", "")[:10],
            reactions=int(item.get("positive_reactions_count", 0) or 0),
            comments=int(item.get("comments_count", 0) or 0),
        )
        reactions += article.reactions
        comments += article.comments
        articles.append(article)

    return {
        "username": dev_username.strip(),
        "articles": articles,
        "stats": {
            "articles": int(profile.get("articles_count", len(articles)) or len(articles)),
            "followers": int(profile.get("followers_count", 0) or 0),
            "reactions_recent": reactions,
            "comments_recent": comments,
        }
    }


def esc(text: str) -> str:
    return saxutils.escape(str(text), {"\"": "&quot;"})


def write_svg(path: Path, title: str, desc: str, body: str, view_box: str = "0 0 1200 220") -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" viewBox="{view_box}" role="img" aria-labelledby="title desc" preserveAspectRatio="xMidYMid meet">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(desc)}</desc>
  {body}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def build_header(config: dict[str, Any]) -> None:
    name = config["display_name"]
    role = config["role"]
    pitch = config["pitch"]
    body = f'''
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#090b1f"/>
    <stop offset="100%" stop-color="#1f1252"/>
  </linearGradient>
</defs>
<rect width="1200" height="220" fill="url(#bg)" rx="18"/>
<circle cx="1040" cy="48" r="3" fill="#fff9"/><circle cx="980" cy="88" r="2" fill="#fff7"/><circle cx="1110" cy="74" r="2.5" fill="#fff8"/>
<text x="60" y="88" fill="#f8f8ff" font-size="56" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{esc(name)}</text>
<text x="60" y="128" fill="#9ab6ff" font-size="27" font-family="Segoe UI, Arial, sans-serif">{esc(role)}</text>
<text x="60" y="170" fill="#c8d4ff" font-size="23" font-family="Segoe UI, Arial, sans-serif">{esc(pitch)}</text>
'''
    write_svg(ASSETS_DIR / "header.svg", f"{name} header banner", f"Role: {role}. Pitch: {pitch}", body)


def build_links(config: dict[str, Any]) -> None:
    names = [
        ("DEV", "dev", "#0a0a0a"),
        ("LinkedIn", "linkedin", "#0a66c2"),
        ("X", "x", "#111111"),
        ("YouTube", "youtube", "#e62117"),
        ("Discord", "discord", "#5865f2"),
    ]
    social = config["social"]
    for index, (label, key, color) in enumerate(names):
        x = 18 + index * 232
        url = social.get(key, "")
        state = "configured" if "your-" not in url and url.endswith(("/",)) is False and "your" not in url else "placeholder"
        body = f'''
<rect width="220" height="54" fill="{color}" rx="12"/>
<circle cx="27" cy="27" r="12" fill="#fff2"/>
<text x="27" y="32" text-anchor="middle" fill="#fff" font-size="14" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{esc(label[0])}</text>
<text x="48" y="33" fill="#fff" font-size="18" font-family="Segoe UI, Arial, sans-serif" font-weight="600">{esc(label)}</text>
<text x="203" y="33" text-anchor="end" fill="#dbe5ff" font-size="11" font-family="Segoe UI, Arial, sans-serif">{state}</text>
'''
        write_svg(LINKS_DIR / f"{key}.svg", f"{label} badge", f"{label} profile link badge", body, "0 0 220 54")

    panel = '<rect width="1200" height="74" rx="14" fill="#0d112f"/><text x="26" y="46" fill="#9bb4ff" font-size="26" font-family="Segoe UI, Arial, sans-serif">Connect</text>'
    panel += ''.join(f'<rect x="{18 + i * 232}" y="10" width="220" height="54" fill="none" rx="12" stroke="#2a3b86"/>' for i in range(5))
    write_svg(ASSETS_DIR / "links.svg", "Social links section", "Row of social links", panel, "0 0 1200 74")


def build_stats(stats: dict[str, Any], projects: list[Project], dev_data: dict[str, Any] | None) -> None:
    total_stars = sum(p.stars for p in projects)
    top_languages = summarize_languages(projects)
    current_streak, longest_streak = calculate_streaks(stats["contribution_days"])

    lines = [
        f"GitHub stars: {total_stars}",
        f"Contributions (last 365 days): {stats['contributions_last_year']}",
        f"Pull requests: {stats['pull_requests']}",
        f"Streak: {current_streak} current, {longest_streak} longest",
        f"Top languages: {', '.join(top_languages) if top_languages else 'N/A'}",
    ]
    if dev_data:
        ds = dev_data["stats"]
        lines.append(f"DEV articles: {ds['articles']} · reactions on latest posts: {ds['reactions_recent']} · comments: {ds['comments_recent']}")
    else:
        lines.append("DEV article stats: unavailable (configure DEV username to enable)")

    body = '<rect width="1200" height="260" rx="18" fill="#0b0f2c"/>'
    body += '<text x="36" y="52" fill="#f5f7ff" font-size="32" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Stats</text>'
    body += '<text x="36" y="82" fill="#9ab0ff" font-size="16" font-family="Segoe UI, Arial, sans-serif">Data source: {}</text>'.format(esc(stats["contribution_source"]))
    for idx, line in enumerate(lines):
        y = 120 + idx * 24
        body += f'<text x="42" y="{y}" fill="#d8e1ff" font-size="18" font-family="Segoe UI, Arial, sans-serif">• {esc(line)}</text>'
    write_svg(ASSETS_DIR / "stats.svg", "GitHub and DEV statistics", "; ".join(lines), body, "0 0 1200 260")


def iso_block(x: float, y: float, w: float, d: float, h: float, colors: tuple[str, str, str]) -> str:
    top_color, left_color, right_color = colors
    top = f"{x},{y-h} {x+w},{y-h-d} {x+2*w},{y-h} {x+w},{y-h+d}"
    left = f"{x},{y-h} {x+w},{y-h+d} {x+w},{y+d} {x},{y}"
    right = f"{x+w},{y-h+d} {x+2*w},{y-h} {x+2*w},{y} {x+w},{y+d}"
    return (
        f'<polygon points="{top}" fill="{top_color}"/>'
        f'<polygon points="{left}" fill="{left_color}"/>'
        f'<polygon points="{right}" fill="{right_color}"/>'
    )


def generate_contribution_city_svg(days: list[dict[str, Any]]) -> str:
    if not days:
        days = fallback_contributions()

    max_count = max((day["count"] for day in days), default=1)
    cell_w = 9
    cell_d = 5
    base_x = 18
    base_y = 340

    skyline = ['<rect width="1200" height="380" fill="#060817" rx="18"/>']
    skyline.append('<ellipse cx="980" cy="80" rx="65" ry="65" fill="#fff2a0" fill-opacity="0.12"/>')
    skyline.append('<text x="28" y="44" fill="#ecf0ff" font-size="30" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Contribution City</text>')

    for idx, day in enumerate(days[-365:]):
        week = idx // 7
        weekday = idx % 7
        x = base_x + week * cell_w * 2 + weekday * 3.2
        y = base_y - week * 1.25 + weekday * 5.8
        norm = day["count"] / max_count if max_count > 0 else 0
        h = 5 + norm * 62
        palette = ("#9ae6ff", "#3677c9", "#4cc3ff") if day["count"] > 0 else ("#47507a", "#2a3152", "#394062")
        skyline.append(iso_block(x, y, cell_w, cell_d, h, palette))

    skyline.append('<text x="28" y="368" fill="#9fb4ff" font-size="14" font-family="Segoe UI, Arial, sans-serif">One building per day over the last 365 days</text>')
    return "\n".join(skyline)


def build_contribution_city(stats: dict[str, Any]) -> None:
    body = generate_contribution_city_svg(stats["contribution_days"])
    total = sum(day["count"] for day in stats["contribution_days"])
    write_svg(
        ASSETS_DIR / "contribution-city.svg",
        "Isometric contribution city skyline",
        f"A building per day based on contribution count. Total contributions represented: {total}.",
        body,
        "0 0 1200 380"
    )


def project_card_svg(project: Project) -> str:
    lang = project.language or "Unknown"
    body = f'''
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0f1335"/><stop offset="100%" stop-color="#22165b"/></linearGradient></defs>
<rect width="580" height="210" fill="url(#bg)" rx="16"/>
<text x="24" y="52" fill="#f4f6ff" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{esc(project.name)}</text>
<text x="24" y="86" fill="#a7bcff" font-size="18" font-family="Segoe UI, Arial, sans-serif">★ {project.stars} · {esc(lang)}</text>
<text x="24" y="124" fill="#d7e0ff" font-size="16" font-family="Segoe UI, Arial, sans-serif">{esc(project.description[:86])}</text>
<rect x="24" y="150" width="170" height="38" rx="10" fill="#4f72ff"/>
<text x="109" y="174" text-anchor="middle" fill="#fff" font-size="15" font-family="Segoe UI, Arial, sans-serif">View repository</text>
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" viewBox="0 0 580 210" role="img" aria-labelledby="title desc" preserveAspectRatio="xMidYMid meet">
  <title id="title">{esc(project.name)} featured project card</title>
  <desc id="desc">{esc(project.description)}</desc>
  {body}
</svg>\n'''


def build_projects(projects: list[Project], username: str) -> None:
    title_body = '<rect width="1200" height="90" fill="#0c102d" rx="16"/><text x="28" y="56" fill="#edf1ff" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Featured Projects</text>'
    write_svg(ASSETS_DIR / "projects.svg", "Featured projects section", "Selected repositories", title_body, "0 0 1200 90")

    by_key = {p.name.lower(): p for p in projects}
    for name in FEATURED_PROJECTS:
        project = by_key.get(name.lower()) or Project(
            name=name,
            url=f"https://github.com/{username}/{name}",
            description="Description not provided in repository metadata."
        )
        path = ASSETS_DIR / f"card-{project.name.lower()}.svg"
        path.write_text(project_card_svg(project), encoding="utf-8")


def build_stack() -> None:
    body = '<rect width="1200" height="260" fill="#0a0f28" rx="16"/>'
    body += '<text x="28" y="50" fill="#edf1ff" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Tech Stack</text>'
    y = 88
    for group, values in STACK.items():
        body += f'<text x="30" y="{y}" fill="#9db4ff" font-size="18" font-family="Segoe UI, Arial, sans-serif">{esc(group)}</text>'
        body += f'<text x="230" y="{y}" fill="#d8e0ff" font-size="18" font-family="Segoe UI, Arial, sans-serif">{esc(", ".join(values))}</text>'
        y += 40
    write_svg(ASSETS_DIR / "stack.svg", "Grouped technology stack", "Languages, frameworks, databases, cloud platforms", body, "0 0 1200 260")


def build_articles(dev_data: dict[str, Any] | None) -> list[Article]:
    title_body = '<rect width="1200" height="90" fill="#0c102d" rx="16"/><text x="28" y="56" fill="#edf1ff" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Latest Articles</text>'
    write_svg(ASSETS_DIR / "writing.svg", "Latest DEV articles section", "Recent writing cards", title_body, "0 0 1200 90")

    articles = dev_data["articles"] if dev_data else []
    if not articles:
        empty = '''
<rect width="1200" height="120" fill="#0a0f28" rx="16"/>
<text x="30" y="64" fill="#dbe4ff" font-size="22" font-family="Segoe UI, Arial, sans-serif">No DEV articles configured yet. Set dev.enabled=true and dev.username in tools/profile/config.json.</text>
'''
        write_svg(WRITING_DIR / "empty.svg", "No DEV articles configured", "Empty state for latest articles", empty, "0 0 1200 120")
        return []

    for idx, article in enumerate(articles, start=1):
        body = f'''
<rect width="1200" height="130" fill="#0a0f28" rx="16"/>
<text x="26" y="46" fill="#f2f5ff" font-size="28" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{esc(article.title[:72])}</text>
<text x="26" y="78" fill="#9eb3ff" font-size="17" font-family="Segoe UI, Arial, sans-serif">Published {esc(article.published_at)}</text>
<text x="26" y="105" fill="#dce5ff" font-size="17" font-family="Segoe UI, Arial, sans-serif">❤ {article.reactions} reactions · 💬 {article.comments} comments</text>
'''
        write_svg(WRITING_DIR / f"post-{idx}.svg", article.title, f"{article.reactions} reactions and {article.comments} comments", body, "0 0 1200 130")

    all_body = '<rect width="1200" height="90" fill="#192253" rx="16"/><text x="600" y="56" text-anchor="middle" fill="#f4f6ff" font-size="30" font-family="Segoe UI, Arial, sans-serif">Read all articles on DEV</text>'
    write_svg(WRITING_DIR / "all-articles.svg", "Read all DEV articles", "Link to all DEV posts", all_body, "0 0 1200 90")
    return articles


def build_footer(config: dict[str, Any]) -> None:
    body = f'''
<defs><linearGradient id="fbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#080b1f"/><stop offset="100%" stop-color="#1a1248"/></linearGradient></defs>
<rect width="1200" height="120" fill="url(#fbg)" rx="16"/>
<text x="42" y="66" fill="#eef2ff" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Thanks for visiting {esc(config['display_name'])}'s profile.</text>
'''
    write_svg(ASSETS_DIR / "footer.svg", "Footer banner", "Profile closing banner", body, "0 0 1200 120")


def build_readme(config: dict[str, Any], projects: list[Project], dev_data: dict[str, Any] | None, articles: list[Article]) -> None:
    social = config["social"]
    username = config["github_username"]
    featured_cards = "\n".join(
        f'<a href="https://github.com/{username}/{name}"><img src="./assets/card-{name.lower()}.svg" width="49%" alt="Featured project card: {name}" /></a>'
        for name in FEATURED_PROJECTS
    )

    catalog_lines = []
    for project in projects:
        catalog_lines.append(f"- [{project.name}]({project.url}) — {project.description}")
    catalog = "\n".join(catalog_lines)

    if articles:
        article_lines = "\n".join(
            f'<a href="{a.url}"><img src="./assets/writing/post-{i}.svg" width="100%" alt="DEV article: {esc(a.title)}" /></a>'
            for i, a in enumerate(articles, start=1)
        )
        article_footer = f'<a href="https://dev.to/{dev_data["username"]}"><img src="./assets/writing/all-articles.svg" width="100%" alt="Read all DEV posts" /></a>'
    else:
        article_lines = '<img src="./assets/writing/empty.svg" width="100%" alt="No DEV articles configured" />'
        article_footer = ""

    content = f'''<p align="center">
<img src="./assets/header.svg" width="100%" alt="Header banner" />
<img src="./assets/links.svg" width="100%" alt="Social links" />
<a href="{social['dev']}"><img src="./assets/links/dev.svg" width="19%" alt="DEV link" /></a><a href="{social['linkedin']}"><img src="./assets/links/linkedin.svg" width="19%" alt="LinkedIn link" /></a><a href="{social['x']}"><img src="./assets/links/x.svg" width="19%" alt="X link" /></a><a href="{social['youtube']}"><img src="./assets/links/youtube.svg" width="19%" alt="YouTube link" /></a><a href="{social['discord']}"><img src="./assets/links/discord.svg" width="19%" alt="Discord link" /></a>
<img src="./assets/stats.svg" width="100%" alt="Stats panel" />
<img src="./assets/contribution-city.svg" width="100%" alt="Contribution city skyline" />
<img src="./assets/projects.svg" width="100%" alt="Featured projects" />
{featured_cards}
<img src="./assets/stack.svg" width="100%" alt="Tech stack" />
<img src="./assets/writing.svg" width="100%" alt="Latest articles" />
{article_lines}
{article_footer}
<img src="./assets/footer.svg" width="100%" alt="Footer banner" />
</p>

## Project Catalog

All currently visible public repositories are listed below.

{catalog}

## Configuration

- Edit `tools/profile/config.json` to set display text and social links.
- Set `dev.enabled=true` and `dev.username` to enable DEV article cards/statistics.
- For best GitHub stats and real contribution calendar data, provide `GITHUB_TOKEN` with public read access.

## Regenerate Locally

```bash
python3 tools/profile/generate.py
python3 -m unittest discover -s tests -p "test_*.py"
```

## Notes

- Contribution city is generated as an original isometric night skyline with one building per day from GitHub contribution data.
- If contribution data cannot be fetched (missing token/rate limits), a deterministic fallback skyline is rendered and labeled in stats.
- No secrets are stored in this repository; configure optional tokens via environment variables in GitHub Actions.
'''
    (ROOT / "README.md").write_text(content, encoding="utf-8")


def run() -> None:
    ensure_dirs()
    config = read_json(CONFIG_PATH)
    token = os.getenv("GITHUB_TOKEN", "").strip() or None

    projects = collect_repo_data(config["github_username"], token)
    gh_stats = collect_github_stats(config["github_username"], token)
    dev_data = collect_dev_data(config.get("dev", {}).get("username", ""), bool(config.get("dev", {}).get("enabled", False)))

    build_header(config)
    build_links(config)
    build_stats(gh_stats, projects, dev_data)
    build_contribution_city(gh_stats)
    build_projects(projects, config["github_username"])
    build_stack()
    articles = build_articles(dev_data)
    build_footer(config)
    build_readme(config, projects, dev_data, articles)


if __name__ == "__main__":
    run()
