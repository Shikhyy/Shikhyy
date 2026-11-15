#!/usr/bin/env python3
"""Generate the animated profile graphics from data/calendar.json.

Usage: python3 scripts/generate.py
Refresh data first with:
  gh api graphql -f query='{user(login:"Shikhyy"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}' --jq '.data.user.contributionsCollection.contributionCalendar' > data/calendar.json
"""
import json
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
cal = json.loads((ROOT / "data/calendar.json").read_text())
weeks = cal["weeks"]
TOTAL = cal["totalContributions"]
days = [(wi, d["weekday"], d["contributionCount"], d["date"])
        for wi, w in enumerate(weeks) for d in w["contributionDays"]]
MX = max(c for _, _, c, _ in days)
ACTIVE = sum(1 for _, _, c, _ in days if c > 0)
nz = sorted(c for _, _, c, _ in days if c > 0)
Q1, Q2, Q3 = nz[len(nz) // 4], nz[len(nz) // 2], nz[3 * len(nz) // 4]


def level(c):
    if c == 0:
        return 0
    return 1 if c <= Q1 else 2 if c <= Q2 else 3 if c <= Q3 else 4


SANS = "'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif"
MONO = "'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif"

DARK = dict(
    t=['#222222', '#4B3A36', '#8C4A3E', '#D84A32', '#FF5A3C'],
    l=['#1A1A1A', '#3A2C29', '#6E3A31', '#A93826', '#C94530'],
    r=['#1E1E1E', '#42332F', '#7B4136', '#BD402B', '#E04F36'])
LIGHT = dict(
    t=['#E4E0D6', '#E0B8AE', '#D98672', '#D2452F', '#B0200F'],
    l=['#D8D3C7', '#C79C92', '#B86A58', '#A8341F', '#8A180A'],
    r=['#DDD8CC', '#D3AAA0', '#C47866', '#BC3A25', '#9C1C0C'])


def lv_vars(p):
    return "".join(f"--t{i}:{p['t'][i]};--l{i}:{p['l'][i]};--r{i}:{p['r'][i]};" for i in range(5))


BASE = (
    ":root{--bg:#111111;--panel:#181818;--card:#1E1E1E;--paper:#F2F0EB;--paperink:#111111;"
    "--ink:#F2F0EB;--mute:#8E8B84;--line:#2A2A2A;--dim:#333333;--accent:#FF5A3C;--brass:#BDB8AC;--ok:#8E8B84;"
    + lv_vars(DARK) + "}"
    "@media (prefers-color-scheme: light){:root{--bg:#F2F0EB;--panel:#E9E6DF;--card:#1E1E1E;--paper:#F2F0EB;--paperink:#111111;"
    "--ink:#111111;--mute:#6B6860;--line:#D9D5CC;--dim:#CFCBC1;--accent:#E8412C;--brass:#55524A;--ok:#8E8B84;"
    + lv_vars(LIGHT) + "}}"
    f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO};font-variant-numeric:tabular-nums}}"
    + "".join(f".t{i}{{fill:var(--t{i})}}.l{i}{{fill:var(--l{i})}}.r{i}{{fill:var(--r{i})}}" for i in range(5))
    + "@keyframes rise{from{opacity:0;transform:translateY(8px)}}"
    "@keyframes grow{from{transform:scaleX(0)}}"
    "@keyframes pop{from{opacity:0;transform:scale(.2)}}"
    "@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
)


def head(w, h, title, desc, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>'
            f"<style>{BASE}{css}</style>"
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" fill="var(--bg)" stroke="var(--line)" stroke-width="2"/>')


def txt(x, y, s, cls="sans", size=13, fill="var(--ink)", weight=400, anchor="start", ls=0, extra=""):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" letter-spacing="{ls*0.45:.2f}" {extra}>{s}</text>')


def save(name, body):
    (OUT / name).write_text(body + "</svg>\n")
    print(name, len(body) // 1024, "KB")


# ---------------------------------------------------------------- tape
def tape():
    W, H = 900, 468
    css = (
        ".reel{transform-box:fill-box;transform-origin:center;animation:spin 3.2s linear infinite}"
        "@keyframes spin{to{transform:rotate(360deg)}}"
        ".prog{transform-box:fill-box;transform-origin:left center;animation:grow 5s cubic-bezier(.3,.6,.2,1) both}"
        ".eq{transform-box:fill-box;transform-origin:center bottom;animation:eq 2.6s ease-in-out infinite}"
        "@keyframes eq{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.6)}}"
        ".row{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}"
    )
    s = [head(W, H, "Recent builds as a mixtape",
              "A cassette card, a tracklist of recent repositories, and an equalizer built from weekly contributions.", css)]
    # cassette
    s.append('<rect x="40" y="34" width="340" height="214" rx="18" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>')
    s.append('<rect x="58" y="50" width="304" height="118" rx="8" fill="var(--paper)"/>')
    s.append('<path d="M58 58a8 8 0 0 1 8-8h288a8 8 0 0 1 8 8v14H58z" fill="var(--accent)"/>')
    s.append(txt(72, 65, "SIDE A / RECENT BUILDS", "mono", 10, "var(--paper)", 700, ls=2))
    s.append(txt(74, 106, "Shikhar Verma", "sans", 22, "var(--paperink)", 800, ls=-0.4))
    s.append(txt(74, 126, "Recent builds, 2026", "sans", 13, "#5E5B54"))
    s.append('<circle cx="326" cy="100" r="22" fill="var(--brass)" stroke="var(--card)" stroke-width="3"/>')
    s.append(txt(326, 106, "SV", "sans", 15, "#1E1B16", 800, "middle"))
    s.append('<rect x="96" y="134" width="228" height="26" rx="13" fill="#121212"/>')
    s.append('<line x1="131" y1="147" x2="289" y2="147" stroke="#3A3A38" stroke-width="2"/>')
    for cx in (122, 298):
        s.append(f'<circle cx="{cx}" cy="147" r="10" fill="var(--paper)"/>'
                 f'<g class="reel" stroke="#121212" stroke-width="2.4" stroke-linecap="round">'
                 + "".join(f'<line x1="{cx}" y1="147" x2="{cx + 7*math.cos(math.radians(a)):.1f}" y2="{147 + 7*math.sin(math.radians(a)):.1f}"/>'
                           for a in (90, 210, 330)) + "</g>"
                 f'<circle cx="{cx}" cy="147" r="2.6" fill="#121212"/>')
    for x, y in ((52, 46), (368, 46), (52, 236), (368, 236)):
        s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#3A3A38"/>')
    s.append('<polygon points="58,185 58,197 67,191" fill="var(--ok)"/>')
    s.append(txt(74, 196, "NOW PLAYING", "mono", 10, "var(--ok)", 700, ls=2))
    s.append(txt(58, 224, "lineage", "sans", 17, "#F2F0EB", 800))
    s.append(txt(362, 224, "TypeScript / Go / Rust", "mono", 10.5, "#8E8B84", anchor="end"))
    s.append('<rect x="58" y="236" width="304" height="4" rx="2" fill="#3A3A38"/>')
    s.append('<rect class="prog" x="58" y="236" width="172" height="4" rx="2" fill="var(--accent)"/>')

    # tracklist
    tracks = [("lineage", "TypeScript", "13 Nov"), ("wiftape", "TypeScript", "11 Nov"),
              ("sangam", "TypeScript", "8 Nov"), ("enfeoff", "TypeScript", "7 Nov"),
              ("orderbook-dst", "Python", "7 Nov"), ("sentinyx", "TypeScript", "4 Nov"),
              ("scythe", "TypeScript", "27 Oct"), ("RippleCI", "Python", "18 Oct")]
    s.append(txt(430, 50, "TRACKLIST", "mono", 11, "var(--ok)", 700, ls=2.4))
    for i, (n, lang, dt) in enumerate(tracks):
        y = 82 + i * 27
        d = 0.15 + i * 0.09
        g = [f'<g class="row" style="animation-delay:{d:.2f}s">']
        if i == 0:
            g.append(f'<rect x="414" y="{y-12}" width="3" height="13" fill="var(--accent)"/><rect x="420" y="{y-12}" width="3" height="13" fill="var(--accent)"/>')
        g.append(txt(430, y, f"{i+1:02d}", "mono", 11, "var(--mute)"))
        g.append(txt(462, y, n, "sans", 15, "var(--ink)", 700))
        g.append(txt(856, y, f"{lang}  /  {dt}", "mono", 11, "var(--mute)", anchor="end"))
        g.append(f'<line x1="430" y1="{y+9}" x2="856" y2="{y+9}" stroke="var(--line)" stroke-width="1"/>')
        g.append("</g>")
        s.append("".join(g))

    # equalizer: weekly totals
    wk = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    mw = max(wk)
    base, mh = 422, 118
    s.append(txt(40, 288, "EQUALIZER / 53 WEEKS", "mono", 11, "var(--mute)", 700, ls=2.4))
    for i, v in enumerate(wk):
        h = max(3.0, mh * math.sqrt(v / mw))
        fill = "var(--accent)" if v >= 0.55 * mw else "var(--brass)" if v >= 0.2 * mw else "var(--dim)"
        s.append(f'<rect class="eq" style="animation-delay:{-(i*0.09)%2.6:.2f}s" x="{40+i*15.5:.1f}" y="{base-h:.1f}" '
                 f'width="11" height="{h:.1f}" rx="2" fill="{fill}"/>')
    s.append(txt(40, 448, f"{TOTAL:,} contributions in the last year / {ACTIVE} active days", "mono", 10.5, "var(--mute)"))
    save("tape.svg", "".join(s))


# ---------------------------------------------------------------- city
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def poly(pts, cls="", extra=""):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return f'<path class="{cls}" d="{d}" {extra}/>'


def city():
    W, H = 900, 560
    a, b = 12.5, 6.25
    ox, oy = 205, 128
    g = 0.86
    nw = len(weeks)

    def P(u, v):
        return (ox + (u - v) * a, oy + (u + v) * b)

    css = (".cb{transform-box:fill-box;transform-origin:50% 100%;animation:up .9s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes up{from{transform:scaleY(.02);opacity:0}}"
           ".cb path{stroke:var(--bg);stroke-width:.6;stroke-linejoin:round}"
           ".st{fill:var(--slabtop)}.sl{fill:var(--slabl)}.sr{fill:var(--slabr)}")
    css = (":root{--slabtop:#1A1A1A;--slabl:#131313;--slabr:#0F0F0F;--grid:#2A2A2A}"
           "@media (prefers-color-scheme: light){:root{--slabtop:#E4E0D6;--slabl:#CBC6BA;--slabr:#BFBAAE;--grid:#D2CDC1}}") + css
    s = [head(W, H, "Contribution city",
              f"An isometric skyline of {TOTAL} contributions over the last year on a bordered base. {ACTIVE} active days, busiest day {MX}.", css)]
    s.append('<defs><radialGradient id="glow" cx="55%" cy="45%" r="60%"><stop offset="0" stop-color="var(--brass)" stop-opacity=".14"/>'
             '<stop offset="1" stop-color="var(--brass)" stop-opacity="0"/></radialGradient></defs>')
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="url(#glow)"/>')

    # base slab with thickness and a visible outline
    u0, u1, v0, v1, th = -0.75, nw - 0.25, -0.75, 6.75, 11
    A, B, C, D = P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)
    s.append(poly([D, C, (C[0], C[1] + th), (D[0], D[1] + th)], "sl"))
    s.append(poly([C, B, (B[0], B[1] + th), (C[0], C[1] + th)], "sr"))
    s.append(poly([A, B, C, D], "st"))
    # grid lines: one per week and per weekday
    grid = []
    for i in range(nw + 1):
        p, q = P(i - 0.5, -0.5), P(i - 0.5, 6.5)
        grid.append(f"M{p[0]:.1f} {p[1]:.1f}L{q[0]:.1f} {q[1]:.1f}")
    for j in range(8):
        p, q = P(-0.5, j - 0.5), P(nw - 0.5, j - 0.5)
        grid.append(f"M{p[0]:.1f} {p[1]:.1f}L{q[0]:.1f} {q[1]:.1f}")
    s.append(f'<path d="{"".join(grid)}" stroke="var(--grid)" stroke-width=".8" fill="none"/>')
    s.append(poly([A, B, C, D], "", 'fill="none" stroke="var(--brass)" stroke-width="1.6" stroke-linejoin="round" opacity=".7"'))
    s.append(poly([D, C, (C[0], C[1] + th), (D[0], D[1] + th)], "", 'fill="none" stroke="var(--brass)" stroke-width="1" opacity=".45" stroke-linejoin="round"'))
    s.append(poly([C, B, (B[0], B[1] + th), (C[0], C[1] + th)], "", 'fill="none" stroke="var(--brass)" stroke-width="1" opacity=".45" stroke-linejoin="round"'))

    # month labels along the front edge
    ang = math.degrees(math.atan2(b, a))
    for wi, dy, c, date in days:
        if date.endswith("-01"):
            x, y = P(wi + dy / 7, v1 + 1.7)
            s.append(f'<text class="mono" x="{x:.1f}" y="{y+th:.1f}" font-size="10" letter-spacing="1.4" fill="var(--mute)" '
                     f'transform="rotate({ang:.1f} {x:.1f} {y+th:.1f})">{MONTHS[int(date[5:7])-1].upper()}</text>')

    # buildings
    a2, b2 = a * g, b * g
    for wi, dy, c, date in sorted(days, key=lambda d: (d[0] + d[1], d[0])):
        sx, sy = P(wi, dy)
        h = 1.4 if c == 0 else 5 + 92 * math.sqrt(c / MX)
        i = level(c)
        top = f"M{sx:.1f} {sy-h-b2:.1f}L{sx+a2:.1f} {sy-h:.1f}L{sx:.1f} {sy-h+b2:.1f}L{sx-a2:.1f} {sy-h:.1f}Z"
        left = f"M{sx-a2:.1f} {sy-h:.1f}L{sx:.1f} {sy-h+b2:.1f}L{sx:.1f} {sy+b2:.1f}L{sx-a2:.1f} {sy:.1f}Z"
        right = f"M{sx:.1f} {sy-h+b2:.1f}L{sx+a2:.1f} {sy-h:.1f}L{sx+a2:.1f} {sy:.1f}L{sx:.1f} {sy+b2:.1f}Z"
        s.append(f'<g class="cb" style="animation-delay:{wi*0.035:.2f}s"><path class="l{i}" d="{left}"/>'
                 f'<path class="r{i}" d="{right}"/><path class="t{i}" d="{top}"/></g>')

    s.append(txt(44, 404, "CONTRIBUTION CITY", "mono", 11, "var(--brass)", 700, ls=2.4))
    s.append(txt(44, 452, f"{TOTAL:,}", "sans", 46, "var(--ink)", 800, ls=-1))
    s.append(txt(44, 476, "contributions in the last year", "sans", 14, "var(--mute)"))
    s.append(txt(44, 504, f"{ACTIVE} active days", "mono", 12, "var(--ink)"))
    s.append(txt(44, 524, f"busiest day: {MX}", "mono", 12, "var(--ink)"))
    # legend
    s.append(txt(676, 542, "LESS", "mono", 10, "var(--mute)", anchor="end", ls=1.2))
    for i in range(5):
        s.append(f'<rect class="t{i}" x="{688+i*16}" y="532" width="12" height="12" rx="2" stroke="var(--line)" stroke-width="1"/>')
    s.append(txt(776, 542, "MORE", "mono", 10, "var(--mute)", ls=1.2))
    save("city.svg", "".join(s))


# ---------------------------------------------------------------- pug
def pug():
    W, H = 900, 440
    rnd = random.Random(11)
    pts = []

    def fib(n):
        ga = math.pi * (3 - math.sqrt(5))
        for i in range(n):
            y = 1 - 2 * (i + .5) / n
            r = math.sqrt(max(0, 1 - y * y))
            yield math.cos(ga * i) * r, y, math.sin(ga * i) * r

    def ell(c, r, n, cls, rotz=0.0, keep=None):
        cz, sz = math.cos(rotz), math.sin(rotz)
        for x, y, z in fib(n):
            if keep and not keep(x, y, z):
                continue
            px, py, pz = x * r[0], y * r[1], z * r[2]
            pts.append((c[0] + px * cz - py * sz, c[1] + px * sz + py * cz, c[2] + pz, cls))

    def cyl(x, z, y0, y1, rad, n, cls):
        for _ in range(n):
            t, yy = rnd.random() * 2 * math.pi, y0 + (y1 - y0) * rnd.random()
            pts.append((x + rad * math.cos(t), yy, z + rad * math.sin(t), cls))

    # stocky body, big round head
    ell((0, 0.05, -0.5), (0.8, 0.62, 1.0), 330, "pf")
    ell((0, 0.88, 0.72), (0.84, 0.74, 0.72), 420, "pf")
    # dark pug mask: muzzle, nose, eyes, ears
    ell((0, 0.72, 1.38), (0.44, 0.32, 0.34), 110, "pm")
    ell((0, 0.86, 1.7), (0.16, 0.11, 0.1), 22, "pn")
    for sx in (-1, 1):
        ell((sx * 0.37, 1.08, 1.28), (0.17, 0.19, 0.14), 34, "pe")
        ell((sx * 0.72, 1.4, 0.55), (0.32, 0.3, 0.13), 70, "pm", rotz=sx * -0.5)
    # forehead wrinkles
    for k in range(3):
        yy = 1.3 + k * 0.1
        for j in range(22):
            x = -0.44 + 0.88 * j / 21
            q = 1 - (x / 0.84) ** 2 - ((yy - 0.88) / 0.74) ** 2
            if q > 0:
                pts.append((x, yy, 0.72 + 0.72 * math.sqrt(q) + 0.02, "pm"))
    # chest patch and cheeks add volume
    ell((0, 0.2, 0.35), (0.55, 0.45, 0.4), 70, "pf")
    # legs and paws
    for lx, lz in ((-0.42, 0.45), (0.42, 0.45), (-0.45, -1.1), (0.45, -1.1)):
        cyl(lx, lz, -1.0, -0.3, 0.2, 42, "pf")
        ell((lx, -0.98, lz + 0.09), (0.25, 0.1, 0.31), 16, "pm")
    # curled tail
    for _ in range(80):
        u, v = rnd.random() * 1.75 * math.pi, rnd.random() * 2 * math.pi
        R, t = 0.3, 0.1
        pts.append((t * math.sin(v), 0.72 + (R + t * math.cos(v)) * math.cos(u), -1.55 + (R + t * math.cos(v)) * math.sin(u), "pf"))

    N, DUR, K = 24, 16, 125
    cx0, cy0, Dd = 450, 236, 9
    start = math.radians(-32)
    out = [head(W, H, "A pug in particles",
                f"A three dimensional pug made of {len(pts)} particles, slowly turning on a turntable.", "")]
    out.append('<ellipse cx="450" cy="402" rx="200" ry="20" fill="var(--line)" opacity=".8"/>')
    out.append('<ellipse cx="450" cy="402" rx="140" ry="12" fill="none" stroke="var(--brass)" stroke-width="1" opacity=".4"/>')
    for x, y, z, cls in sorted(pts, key=lambda p: p[2]):
        cxs, rs = [], []
        for f in range(N + 1):
            th = start + 2 * math.pi * f / N
            x1 = x * math.cos(th) + z * math.sin(th)
            z1 = -x * math.sin(th) + z * math.cos(th)
            pr = Dd / (Dd - z1)
            cxs.append(f"{cx0 + K * x1 * pr:.0f}")
            rs.append(f"{max(0.7, 1.9 * pr * (0.62 + 0.2 * z1)):.1f}")
        cy = cy0 - K * (y - 0.28)
        out.append(f'<circle class="{cls}" cx="{cxs[0]}" cy="{cy:.0f}" r="{rs[0]}">'
                   f'<animate attributeName="cx" values="{";".join(cxs)}" dur="{DUR}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="r" values="{";".join(rs)}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    out.append(txt(44, 46, "A PUG, IN PARTICLES", "mono", 11, "var(--brass)", 700, ls=2.4))
    out.append(txt(856, 46, f"{len(pts)} PARTICLES / ONE TURN EVERY {DUR} S", "mono", 11, "var(--mute)", anchor="end", ls=1.2))
    css = ".pf{fill:var(--brass)}.pm{fill:var(--accent)}.pe{fill:var(--ink)}.pn{fill:var(--ink)}"
    save("pug.svg", "".join(out).replace("<style>", "<style>" + css, 1))


# ---------------------------------------------------------------- invaders
def invaders():
    W, H = 900, 282
    step, cs = 16, 13
    x0, y0 = 28, 84
    T = 14.0
    travel = 832.0
    ship_y = 244
    top = sorted(days, key=lambda d: -d[2])[:12]
    targets = {(d[0], d[1]): d for d in top}
    css = [
        f".ship{{animation:sail {T}s linear infinite}}",
        f"@keyframes sail{{from{{transform:translateX(0)}}to{{transform:translateX({travel}px)}}}}",
        ".bul{animation:shot .9s linear infinite}",
        "@keyframes shot{0%{transform:translateY(0);opacity:1}85%{opacity:1}100%{transform:translateY(-44px);opacity:0}}",
        ".tg{transform-box:fill-box;transform-origin:center}",
    ]
    for i, (key, d) in enumerate(targets.items()):
        xc = x0 + key[0] * step + cs / 2
        p = min(88.0, max(4.0, (xc - 36) / travel * 100))
        css.append(f"@keyframes k{i}{{0%,{p-2:.1f}%{{opacity:1;transform:scale(1)}}{p:.1f}%{{opacity:1;transform:scale(1.45)}}"
                   f"{p+3:.1f}%,92%{{opacity:0;transform:scale(.2)}}98%,100%{{opacity:1;transform:scale(1)}}}}"
                   f".tg{i}{{animation:k{i} {T}s linear infinite}}")
    s = [head(W, H, "Contribution invaders",
              "A year of daily contributions as a grid. A ship sweeps underneath and shoots the twelve busiest days.", "".join(css))]
    s.append(txt(28, 44, "CONTRIBUTION INVADERS", "mono", 11, "var(--brass)", 700, ls=2.4))
    s.append(txt(872, 44, f"TARGETS: THE 12 BUSIEST DAYS / PEAK {MX}", "mono", 11, "var(--mute)", anchor="end", ls=1.2))
    rnd = random.Random(7)
    for k in range(18):
        s.append(f'<circle cx="{rnd.randint(14,886)}" cy="{rnd.randint(54,270)}" r="1.2" fill="var(--mute)" '
                 f'style="animation:pulse {2+rnd.random()*3:.1f}s {-rnd.random()*4:.1f}s ease-in-out infinite"/>')
    for wi, dy, c, date in days:
        x, y = x0 + wi * step, y0 + dy * step
        i = level(c)
        if (wi, dy) in targets:
            idx = list(targets).index((wi, dy))
            s.append(f'<g class="tg tg{idx}"><rect class="t{i}" x="{x}" y="{y}" width="{cs}" height="{cs}" rx="3"/>'
                     f'<circle cx="{x+cs/2}" cy="{y+cs/2}" r="11" fill="none" stroke="var(--accent)" stroke-width="1.6"/></g>')
        else:
            s.append(f'<rect class="t{i}" x="{x}" y="{y}" width="{cs}" height="{cs}" rx="3"/>')
    s.append(f'<g transform="translate(36,{ship_y})"><g class="ship">'
             '<rect class="bul" x="-1.5" y="-26" width="3" height="10" rx="1.5" fill="var(--brass)"/>'
             '<rect class="bul" style="animation-delay:-.45s" x="-1.5" y="-26" width="3" height="10" rx="1.5" fill="var(--brass)"/>'
             '<polygon points="0,-14 11,8 5,4 0,9 -5,4 -11,8" fill="var(--accent)"/>'
             '<circle cx="0" cy="-2" r="2.6" fill="var(--brass)"/></g></g>')
    save("invaders.svg", "".join(s))


# ---------------------------------------------------------------- stack
def stack():
    W, H = 900, 350
    langs = [("TypeScript", "TS", 33, "var(--accent)"), ("Python", "PY", 7, "var(--brass)"),
             ("HTML", "HT", 3, "var(--ok)"), ("JavaScript", "JS", 3, "var(--brass)"),
             ("Kotlin", "KT", 1, "var(--accent)"), ("Rust", "RS", 1, "var(--ok)"), ("Solidity", "SO", 1, "var(--mute)")]
    tot = sum(n for _, _, n, _ in langs)
    css = ".blk{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,1.4,.4,1) both}"
    s = [head(W, H, "Genres: languages by repository",
              f"Primary language across {tot} public repositories.", css)]
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="var(--panel)" stroke="var(--line)" stroke-width="2"/>')
    s.append(f'<path d="M1 9a8 8 0 0 1 8-8h{W-18}a8 8 0 0 1 8 8v24H1z" fill="var(--accent)"/>')
    s.append(txt(28, 25, f"GENRES / LANGUAGES ACROSS {tot} REPOSITORIES", "mono", 11, "var(--paper)", 700, ls=2.4))
    for r, (name, code, n, col) in enumerate(langs):
        y = 66 + r * 38
        pct = n / tot * 100
        filled = max(1, round(pct / 100 * 25))
        s.append(f'<rect x="28" y="{y-4}" width="26" height="26" rx="7" fill="none" stroke="{col}" stroke-width="2"/>')
        s.append(txt(41, y+14, code, "mono", 10, col, 800, "middle"))
        s.append(txt(68, y+15, name, "sans", 15, "var(--ink)", 700))
        for j in range(25):
            fill = col if j < filled else "var(--dim)"
            op = "" if j < filled else ' opacity=".55"'
            s.append(f'<rect class="blk" style="animation-delay:{r*0.12+j*0.025:.2f}s" x="{230+j*21}" y="{y+1}" width="16" height="16" rx="3" fill="{fill}"{op}/>')
        s.append(txt(872, y+15, f"{pct:.0f}%", "mono", 13, "var(--mute)", 700, "end"))
    save("stack.svg", "".join(s))


# ---------------------------------------------------------------- tools marquee
def tools():
    W, H = 900, 150
    rows = [
        (["TypeScript", "Python", "Go", "Rust", "Kotlin", "Solidity", "JavaScript", "Next.js", "Vercel", "Docker"], 1),
        (["Solana", "Chainlink", "Robinhood Chain", "Snowflake", "DuckDB", "FalkorDB", "PostgreSQL", "Cypher", "pnpm", "LLM agents"], -1),
    ]
    cols = ["var(--accent)", "var(--brass)", "var(--ok)"]
    css = []
    body = []
    for ri, (items, direction) in enumerate(rows):
        widths = [len(t) * 7.9 + 46 for t in items]
        gap = 12
        total = sum(widths) + gap * len(items)
        dur = total / 55
        css.append(f"@keyframes m{ri}{{from{{transform:translateX({0 if direction>0 else -total:.0f}px)}}"
                   f"to{{transform:translateX({-total if direction>0 else 0:.0f}px)}}}}.m{ri}{{animation:m{ri} {dur:.0f}s linear infinite}}")
        y = 24 + ri * 56
        g = [f'<g class="m{ri}">']
        for copy in range(3):
            x = copy * total
            for k, (t, w) in enumerate(zip(items, widths)):
                col = cols[(k + ri) % 3]
                g.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="var(--panel)" stroke="var(--line)" stroke-width="1.5"/>'
                         f'<circle cx="{x+20:.0f}" cy="{y+19}" r="4.5" fill="{col}"/>'
                         + txt(f"{x+34:.0f}", y + 24, t, "sans", 14, "var(--ink)", 600))
                x += w + gap
        g.append("</g>")
        body.append("".join(g))
    s = [head(W, H, "Tools I reach for", "Two rows of scrolling chips naming languages, frameworks, chains and data tools.", "".join(css))]
    s.append('<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".08" stop-color="#fff"/>'
             '<stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
             f'<mask id="mk"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>')
    s.append('<g mask="url(#mk)">' + "".join(body) + "</g>")
    save("tools.svg", "".join(s))


# ---------------------------------------------------------------- hero
GLYPHS = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
}
HERO_WORD = ("SHIKHYY",)

HERO_THEMES = {
    "light": dict(bg="#F2F0EB", line="#D9D5CC", ink="#111111", soft="#3A3833", mute="#6B6860", dim="#E0DCD2",
                  chip="#E7E3DA", accent="#E8412C", glow=".07"),
    "dark": dict(bg="#111214", line="#26282C", ink="#F2F0EB", soft="#C9C6BE", mute="#8E8B84", dim="#2A2C30",
                 chip="#1B1D20", accent="#FF5A3C", glow=".11"),
}


def hero():
    """Opaque banner in two themes, so it reads correctly on any page background."""
    W, H = 900, 324
    cell, step, cols, rows = 13, 16.5, 47, 7
    x0, y0 = 62, 30
    red = set()
    for line_no, word in enumerate(HERO_WORD):
        for li, ch in enumerate(word):
            for r in range(7):
                for c in range(5):
                    if GLYPHS[ch][r][c] == "#":
                        red.add((li * 7 + c, line_no * 8 + r))
    for name, t in HERO_THEMES.items():
        rnd = random.Random(3)
        css = (f".sans{{font-family:{SANS}}}"
               ".in{animation:in .9s cubic-bezier(.2,.8,.2,1) both}@keyframes in{from{opacity:0;transform:translateY(10px)}}"
               ".bar{transform-box:fill-box;transform-origin:left center;animation:bar .8s cubic-bezier(.6,0,.2,1) .1s both}@keyframes bar{from{transform:scaleX(0)}}"
               ".sq{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,1.4,.4,1) both,wave 3.2s ease-in-out infinite}"
               "@keyframes pop{from{opacity:0;transform:scale(.2)}}@keyframes wave{0%,100%{opacity:1}50%{opacity:.72}}"
               ".sh{animation:sh 4s ease-in-out infinite}@keyframes sh{0%,100%{opacity:.18}50%{opacity:.55}}"
               "@media (prefers-reduced-motion: reduce){*{animation:none!important}}")
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">'
             '<title id="t">Shikhar Verma</title><desc id="d">Shikhar Verma, Shikhyy on GitHub. Third-year B.Tech student at NIT Tiruchirappalli building AI agent guardrails, secure payments and evals.</desc>'
             f"<style>{css}</style>"
             f'<defs><radialGradient id="g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="{t["glow"]}"/>'
             f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient></defs>'
             f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>'
             f'<ellipse cx="450" cy="92" rx="430" ry="130" fill="url(#g)"/>',
             f'<rect class="bar" x="62" y="166" width="40" height="5" fill="{t["accent"]}"/>',
             f'<text class="sans in" style="animation-delay:.2s" x="60" y="232" font-size="64" font-weight="700" letter-spacing="-2" fill="{t["ink"]}">Shikhar Verma</text>',
             f'<text class="sans in" style="animation-delay:.4s" x="62" y="270" font-size="19" fill="{t["soft"]}">Third-year B.Tech student at NIT Tiruchirappalli.</text>',
             f'<text class="sans in" style="animation-delay:.5s" x="62" y="296" font-size="19" fill="{t["soft"]}">Building AI agent guardrails, secure payments and evals.</text>']
        for r in range(rows):
            for c in range(cols):
                gx, gy = x0 + c * step, y0 + r * step
                if (c, r) in red:
                    d = 0.5 + c * 0.03 + r * 0.02
                    o.append(f'<rect class="sq" style="animation-delay:{d:.2f}s,{1.6 + c*0.05:.2f}s" x="{gx}" y="{gy}" width="{cell}" height="{cell}" rx="3" fill="{t["accent"]}"/>')
                else:
                    o.append(f'<rect class="sh" style="animation-delay:{-rnd.random()*4:.2f}s;animation-duration:{3+rnd.random()*3:.1f}s" '
                             f'x="{gx}" y="{gy}" width="{cell}" height="{cell}" rx="3" fill="{t["dim"]}"/>')
        o.append("</svg>\n")
        (OUT / f"hero-{name}.svg").write_text("".join(o))
    print("hero-light.svg, hero-dark.svg")


# ---------------------------------------------------------------- stats card
def streaks():
    c = [n for _, _, n, _ in sorted(days, key=lambda d: (d[0], d[1]))]
    best = run = 0
    for v in c:
        run = run + 1 if v > 0 else 0
        best = max(best, run)
    i = len(c) - 1
    if c[i] == 0:
        i -= 1
    cur = 0
    while i >= 0 and c[i] > 0:
        cur += 1
        i -= 1
    return best, cur


def stats():
    st = json.loads((ROOT / "data/stats.json").read_text())
    best, cur = streaks()
    W, H = 900, 312
    css = (".up{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}"
           ".line{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 2.2s cubic-bezier(.5,0,.2,1) .4s both}"
           "@keyframes draw{from{stroke-dashoffset:1}}"
           ".area{animation:fadein 1.6s ease-out 1.2s both}@keyframes fadein{from{opacity:0}}")
    s = [head(W, H, "GitHub in numbers",
              f"{st['commits']:,} commits in the last year, {st['prs']} pull requests with {st['merged']} merged, "
              f"contributions to {st['contributedTo']} projects outside my own, {st['pubRepos']} original repositories. "
              f"Longest streak {best} days, current streak {cur} days.", css)]
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="var(--panel)" stroke="var(--line)" stroke-width="2"/>')
    s.append(f'<path d="M1 9a8 8 0 0 1 8-8h{W-18}a8 8 0 0 1 8 8v24H1z" fill="var(--accent)"/>')
    s.append(txt(28, 25, "GITHUB IN NUMBERS", "mono", 11, "var(--paper)", 700, ls=2.4))
    s.append(txt(872, 25, "LAST 12 MONTHS", "mono", 11, "var(--paper)", 700, anchor="end", ls=2.4))
    since = datetime_month(st["createdAt"])
    metrics = [
        (f"{st['commits']:,}", "commits", "in the last 12 months"),
        (f"{st['prs']}", "pull requests", f"{st['merged']} merged"),
        (f"{st['contributedTo']}", "outside projects", "contributed to beyond my own repos"),
        (f"{st['pubRepos']}", "original repositories", "not counting forks"),
    ]
    for i, (num, lab, sub) in enumerate(metrics):
        x = 36 + i * 212
        s.append(f'<g class="up" style="animation-delay:{0.1+i*0.12:.2f}s">'
                 + txt(x, 98, num, "sans", 44, "var(--ink)", 800, ls=-1.2)
                 + txt(x, 124, lab, "sans", 14, "var(--ink)", 600)
                 + txt(x, 142, sub, "sans", 12, "var(--mute)") + "</g>")
    # weekly sparkline
    wk = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    mw = max(wk)
    X0, X1, YB, YT = 36, 864, 252, 168
    pts_ = [(X0 + (X1 - X0) * i / (len(wk) - 1), YB - (YB - YT) * math.sqrt(v / mw)) for i, v in enumerate(wk)]
    d_line = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts_)
    d_area = d_line + f"L{X1} {YB}L{X0} {YB}Z"
    s.append(f'<path class="area" d="{d_area}" fill="var(--accent)" opacity=".16"/>')
    s.append(f'<path class="line" pathLength="1" d="{d_line}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="var(--line)" stroke-width="1.5"/>')
    # streak row
    items = [(f"{best} days", "longest streak"), (f"{cur} days", "current streak"),
             (f"{ACTIVE}", "active days of 365"), (since, "on GitHub since")]
    for i, (a_, b_) in enumerate(items):
        x = 36 + i * 212
        s.append(f'<text class="sans" x="{x}" y="288" font-size="13" fill="var(--mute)">'
                 f'<tspan font-weight="700" fill="var(--ink)">{a_}</tspan>  {b_}</text>')
    save("stats.svg", "".join(s))


def datetime_month(iso):
    import datetime
    d = datetime.date.fromisoformat(iso[:10])
    return d.strftime("%b %Y")


# ---------------------------------------------------------------- game data
def game_data():
    out = ROOT / "web/invaders"
    out.mkdir(parents=True, exist_ok=True)
    grid = [[0] * 7 for _ in weeks]
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            grid[wi][d["weekday"]] = d["contributionCount"]
    last = weeks[-1]["contributionDays"][-1]["date"]
    payload = {"total": TOTAL, "active": ACTIVE, "max": MX, "asOf": last, "weeks": grid}
    (out / "data.js").write_text("window.CONTRIB=" + json.dumps(payload, separators=(",", ":")) + ";\n")
    print("web/invaders/data.js", len(weeks), "weeks")


# ---------------------------------------------------------------- orderbook results
def results():
    rows = [("nemotron_ultra", 100.0, False), ("mistral_large", 93.9, False), ("gemini_35_flash", 87.5, True),
            ("gemma_26b", 81.8, False), ("flash_lite", 78.8, False), ("nemotron_nano", 36.4, False), ("ministral_8b", 36.4, False)]
    W, H = 900, 330
    css = (".bar{transform-box:fill-box;transform-origin:left center;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both}"
           ".row{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}")
    s = [head(W, H, "OrderBook-DST pass rates",
              "Pass rate on the 11 implementation tasks for seven free-tier models: nemotron_ultra 100%, mistral_large 93.9%, "
              "gemini_35_flash 87.5% (incomplete), gemma_26b 81.8%, flash_lite 78.8%, nemotron_nano 36.4%, ministral_8b 36.4%.", css)]
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="var(--panel)" stroke="var(--line)" stroke-width="2"/>')
    s.append(f'<path d="M1 9a8 8 0 0 1 8-8h{W-18}a8 8 0 0 1 8 8v24H1z" fill="var(--accent)"/>')
    s.append(txt(28, 25, "ORDERBOOK-DST  /  PASS RATE ON THE 11 IMPLEMENTATION TASKS", "mono", 11, "var(--paper)", 700, ls=2.4))
    X0, TRACK = 190, 560
    for i, (name, pct, inc) in enumerate(rows):
        y = 62 + i * 34
        w = TRACK * pct / 100
        col = "var(--accent)" if pct >= 78 else "var(--brass)"
        s.append(f'<g class="row" style="animation-delay:{i*0.08:.2f}s">'
                 + txt(28, y + 14, name, "sans", 14, "var(--ink)", 600)
                 + f'<rect x="{X0}" y="{y}" width="{TRACK}" height="20" rx="4" fill="var(--dim)" opacity=".55"/></g>')
        if inc:
            s.append(f'<rect class="bar" style="animation-delay:{i*0.08+0.2:.2f}s" x="{X0}" y="{y}" width="{w:.0f}" height="20" rx="4" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="5 4"/>')
        else:
            s.append(f'<rect class="bar" style="animation-delay:{i*0.08+0.2:.2f}s" x="{X0}" y="{y}" width="{w:.0f}" height="20" rx="4" fill="{col}"/>')
        label = f"{pct:.1f}%" + ("  incomplete" if inc else "")
        s.append(txt(X0 + TRACK + 16, y + 15, label, "mono", 13, "var(--ink)", 700))
    s.append(txt(28, 316, "329 real trials, 7 free-tier models, 3 trials per task. Pass means every hidden check and all 20 seeded 200-event simulations. Dashed: rate-limited, incomplete.", "sans", 11.5, "var(--mute)"))
    save("results.svg", "".join(s))



# ---------------------------------------------------------------- resilientpay results
def resilient():
    tiles = [
        ("98.5%", "NFC success", ["19.7 ms, 1,000 transactions", "across 5 channels"]),
        ("93.0%", "SMS fallback delivery", ["over degraded cellular links"]),
        ("62.3%", "smaller payloads", ["106 B against 281 B for JSON,", "SMS segments cut from 4 to 2"]),
        ("0", "false acceptances", ["2,000 fault-injected transactions,", "100% convergence"]),
        ("0 paise", "undetected exposure", ["900 double-spend and replay trials,", "caught by the second transaction"]),
        ("3.2x / 7.2x", "hash chain vs Merkle audit", ["faster writes, faster", "verification"]),
    ]
    W, H = 900, 352
    css = ".up{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}"
    s = [head(W, H, "ResilientPay: what the simulator measured",
              "Six results from ResilientPay's deterministic simulation: 98.5 percent NFC success, 93.0 percent SMS fallback delivery, "
              "62.3 percent smaller payloads, zero false acceptances across 2,000 fault-injected transactions, zero paise of undetected "
              "exposure across 900 double-spend trials, and a hash-chain audit log 3.2 times faster on writes and 7.2 times faster to verify.", css)]
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="var(--panel)" stroke="var(--line)" stroke-width="2"/>')
    s.append(f'<path d="M1 9a8 8 0 0 1 8-8h{W-18}a8 8 0 0 1 8 8v24H1z" fill="var(--accent)"/>')
    s.append(txt(28, 25, "RESILIENTPAY  /  WHAT THE SIMULATOR MEASURED", "mono", 11, "var(--paper)", 700, ls=2.4))
    tw, th, gap = 268, 122, 12
    for i, (num, lab, sub) in enumerate(tiles):
        x = 36 + (i % 3) * (tw + gap)
        y = 56 + (i // 3) * (th + gap)
        col = "var(--accent)" if i in (3, 4) else "var(--ink)"
        g = [f'<g class="up" style="animation-delay:{i*0.09:.2f}s">',
             f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="var(--bg)" stroke="var(--line)" stroke-width="1.5"/>',
             txt(x + 20, y + 52, num, "sans", 38, col, 800, ls=-1),
             txt(x + 20, y + 78, lab, "sans", 14, "var(--ink)", 600)]
        for k, line in enumerate(sub):
            g.append(txt(x + 20, y + 98 + k * 15, line, "sans", 12, "var(--mute)"))
        g.append("</g>")
        s.append("".join(g))
    s.append(txt(36, 338, "Deterministic simulation with test identities and simulated value. Not real payments.", "sans", 12, "var(--mute)"))
    save("resilientpay.svg", "".join(s))



if __name__ == "__main__":
    tape()
    city()
    invaders()
    stack()
    hero()
    stats()
    results()
    resilient()
    game_data()
