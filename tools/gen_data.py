#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Veri paneli: gerçek GitHub verisinden diller, çalışma saatleri, satırlar.

lowlighter/metrics'in fikri, sayfanın kendi diliyle. Kaynaklar:
  - diller     : GraphQL, katkıda bulunulan TÜM depolar (özel + org), son 365 günde push alanlar
  - saat/gün   : REST /users/<login>/events (kimlik doğrulamalı → özel push'lar dahil), son 30 gün
  - satırlar   : REST /repos/<r>/stats/contributors, en son push alan N depo (202 → bekle → tekrar)

Token: METRICS_TOKEN (Action secret) ya da yerelde `gh auth token`. Token yoksa
script 0 ile çıkar ve mevcut dosyalara dokunmaz — Action kırılmaz, veri sabit kalır.
"""
import collections, datetime, json, os, pathlib, subprocess, sys, time, urllib.request, zoneinfo

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
TZ = zoneinfo.ZoneInfo("Europe/Istanbul")
GUN = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
LANG_COLOR = {"JavaScript": "#F1E05A", "TypeScript": "#3178C6", "HTML": "#E34C26", "PLpgSQL": "#336790",
              "Dart": "#00B4AB", "PHP": "#4F5D95", "Python": "#3572A5", "CSS": "#663399",
              "Blade": "#F7523F", "PLSQL": "#DAD8D8", "Shell": "#89E051", "C#": "#178600",
              "Java": "#B07219", "SCSS": "#C6538C", "Vue": "#41B883", "Dockerfile": "#384D54"}
SKIP_LANG = {"Blade", "PLSQL", "Makefile", "Batchfile", "Procfile", "Dockerfile"}

LIGHT = dict(name="light", card="#F6F8FA", edge="#D0D7DE", ink="#1F2328", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", track="#E4E8EC", rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0E141B", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#6E7681", ok="#3FB950", track="#21262D", rim="#FFFFFF", rim_a=0.075)


def token():
    t = os.environ.get("METRICS_TOKEN", "").strip()
    if t:
        return t
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def api(url, tok, method="GET", body=None, retries=3):
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"bearer {tok}", "Accept": "application/vnd.github+json",
        "User-Agent": "profil-veri", "Content-Type": "application/json"})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status == 202:                 # istatistik henüz hazırlanıyor
                    time.sleep(3 + i*2); continue
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 202:
                time.sleep(3 + i*2); continue
            raise
    return None


def gql(q, tok):
    return api("https://api.github.com/graphql", tok, "POST", json.dumps({"query": q}).encode())


def tr(n):
    return f"{n:,}".replace(",", ".")


def kisa(n):
    return f"{n/1_000_000:.1f}M".replace(".", ",") if n >= 1_000_000 else (f"{n/1000:.0f}K" if n >= 10_000 else tr(n))


# ── veri ─────────────────────────────────────────────────────────────────
def fetch(tok):
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)).isoformat()
    d = gql('''query { viewer { repositories(first:100, affiliations:[OWNER,COLLABORATOR,ORGANIZATION_MEMBER],
              orderBy:{field:PUSHED_AT, direction:DESC}) { nodes { nameWithOwner pushedAt isFork
              languages(first:10, orderBy:{field:SIZE, direction:DESC}) { edges { size node { name } } } } } } }''', tok)
    repos = [r for r in d["data"]["viewer"]["repositories"]["nodes"] if not r["isFork"] and r["pushedAt"] >= since]
    lang = collections.Counter()
    for r in repos:
        for e in r["languages"]["edges"]:
            if e["node"]["name"] not in SKIP_LANG:
                lang[e["node"]["name"]] += e["size"]
    total = sum(lang.values()) or 1
    langs = [(n, 100*s/total) for n, s in lang.most_common(7)]

    # olaylar
    now = datetime.datetime.now(datetime.timezone.utc)
    hours, wdays, pushes, commits = collections.Counter(), collections.Counter(), 0, 0
    for page in range(1, 4):
        ev = api(f"https://api.github.com/users/{USER}/events?per_page=100&page={page}", tok) or []
        if not ev:
            break
        for e in ev:
            if e["type"] != "PushEvent":
                continue
            t = datetime.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00"))
            if (now - t).days > 30:
                continue
            lt = t.astimezone(TZ)
            hours[lt.hour] += 1; wdays[lt.weekday()] += 1; pushes += 1
            commits += int(e.get("payload", {}).get("size") or 1)

    # satırlar: son push alan 12 depo
    add = dele = comm = 0; used = 0
    for r in repos[:12]:
        st = api(f"https://api.github.com/repos/{r['nameWithOwner']}/stats/contributors", tok)
        if not st:
            continue
        for c in st:
            if c.get("author") and c["author"]["login"].lower() == USER:
                add += sum(w["a"] for w in c["weeks"]); dele += sum(w["d"] for w in c["weeks"])
                comm += sum(w["c"] for w in c["weeks"]); used += 1
    return dict(langs=langs, repos=len(repos), hours=hours, wdays=wdays, pushes=pushes,
                commits=commits, add=add, dele=dele, comm=comm, used=used)


# ── görsel ───────────────────────────────────────────────────────────────
def build(p, v):
    W, H = 1000, 372
    CYC, FILL, HOLD = 17.0, 5.0, 9.0
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')

    def lab(x, y, t, anchor="start"):
        o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="9.5" '
                 f'letter-spacing="2.2" fill="{p["faint"]}">{t}</text>')

    def grow(i, n):
        t = FILL * (i / max(1, n))
        k1 = round(t/CYC, 5); k2 = round((t+0.9)/CYC, 5)
        k3 = round((FILL+HOLD)/CYC, 5); k4 = round((FILL+HOLD+0.6)/CYC, 5)
        return k1, k2, k3, k4

    # ── DİLLER (sol üst) ─────────────────────────────────────────────
    lab(28, 30, "DİLLER")
    lab(556, 30, f"{v['repos']} depo · son 365 gün", "end")
    LX, LW, LY = 28, 528, 48
    mx = max((s for _, s in v["langs"]), default=1)
    for i, (n, s) in enumerate(v["langs"]):
        y = LY + i*24
        bw = round(LW*0.62 * s/mx, 1)
        col = LANG_COLOR.get(n, p["sub"])
        k1, k2, k3, k4 = grow(i, len(v["langs"]))
        o.append(f'<text x="{LX}" y="{y+10}" font-family="{MONO}" font-size="11.5" fill="{p["ink"]}">{n}</text>')
        o.append(f'<rect x="{LX+118}" y="{y}" width="{LW*0.62:.0f}" height="12" rx="3" fill="{p["track"]}"/>')
        o.append(f'<rect x="{LX+118}" y="{y}" width="0" height="12" rx="3" fill="{col}">'
                 f'<animate attributeName="width" values="0;0;{bw};{bw};0;0" keyTimes="0;{k1};{k2};{k3};{k4};1" '
                 f'dur="{CYC}s" repeatCount="indefinite"/></rect>')
        o.append(f'<text x="{LX+LW}" y="{y+10}" text-anchor="end" font-family="{MONO}" font-size="11" '
                 f'fill="{p["sub"]}">%{s:.1f}'.replace(".", ",") + '</text>')

    # ── SATIRLAR (sağ üst) ───────────────────────────────────────────
    o.append(f'<line x1="588" y1="22" x2="588" y2="212" stroke="{p["edge"]}"/>')
    lab(612, 30, "SON BİR YIL")
    stats = [(f"+{kisa(v['add'])}", "eklenen satır", p["ok"]), (f"−{kisa(v['dele'])}", "silinen satır", "#F85149"),
             (tr(v["comm"]), "commit", p["ink"])]
    for i, (num, l, col) in enumerate(stats):
        y = 76 + i*46
        o.append(f'<text x="612" y="{y}" font-family="{MONO}" font-size="24" font-weight="700" fill="{col}">{num}</text>')
        o.append(f'<text x="614" y="{y+17}" font-family="{MONO}" font-size="9.5" letter-spacing="1.2" fill="{p["faint"]}">{l}</text>')
    o.append(f'<text x="612" y="206" font-family="{MONO}" font-size="9" fill="{p["faint"]}">'
             f'en son push alan {v["used"]} depoda, yazar olarak</text>')

    # ── ÇALIŞMA SAATİ + HAFTANIN GÜNÜ (alt) ──────────────────────────
    o.append(f'<line x1="28" y1="230" x2="{W-28}" y2="230" stroke="{p["edge"]}"/>')
    lab(28, 254, "ÇALIŞMA SAATİ")
    lab(556, 254, f"{v['pushes']} push · {tr(v['commits'])} commit · son 30 gün", "end")
    BASE, MAXH = 344, 68
    hv = [v["hours"].get(h, 0) for h in range(24)]; hm = max(hv) or 1; peak = hv.index(hm)
    span = 528/24; bw = span*0.62
    for i, c in enumerate(hv):
        h = max(1.5, MAXH*c/hm); x = 28 + i*span + (span-bw)/2
        k1, k2, k3, k4 = grow(i, 31)
        o.append(f'<rect x="{x:.1f}" y="{BASE}" width="{bw:.1f}" height="0" rx="2" fill="{p["ok"] if i==peak else p["track"]}">'
                 f'<animate attributeName="height" values="0;0;{h:.1f};{h:.1f};0;0" keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{BASE};{BASE};{BASE-h:.1f};{BASE-h:.1f};{BASE};{BASE}" keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                 f'<title>{i:02d}:00 — {c} push</title></rect>')
        if i % 3 == 0:
            o.append(f'<text x="{x+bw/2:.1f}" y="{BASE+14}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{p["faint"]}">{i:02d}</text>')
    o.append(f'<line x1="28" y1="{BASE+1}" x2="556" y2="{BASE+1}" stroke="{p["edge"]}"/>')

    lab(612, 254, "HAFTANIN GÜNÜ")
    wv = [v["wdays"].get(d, 0) for d in range(7)]; wm = max(wv) or 1; wpeak = wv.index(wm)
    span2 = 360/7; bw2 = span2*0.6
    for i, c in enumerate(wv):
        h = max(1.5, MAXH*c/wm); x = 612 + i*span2 + (span2-bw2)/2
        k1, k2, k3, k4 = grow(24+i, 31)
        o.append(f'<rect x="{x:.1f}" y="{BASE}" width="{bw2:.1f}" height="0" rx="2" fill="{p["ok"] if i==wpeak else p["track"]}">'
                 f'<animate attributeName="height" values="0;0;{h:.1f};{h:.1f};0;0" keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{BASE};{BASE};{BASE-h:.1f};{BASE-h:.1f};{BASE};{BASE}" keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                 f'<title>{GUN[i]} — {c} push</title></rect>')
        o.append(f'<text x="{x+bw2/2:.1f}" y="{BASE+14}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{p["faint"]}">{GUN[i]}</text>')
    o.append(f'<line x1="612" y1="{BASE+1}" x2="{W-28}" y2="{BASE+1}" stroke="{p["edge"]}"/>')

    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    lg = ", ".join(f"{n} %{s:.0f}" for n, s in v["langs"][:4])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Diller: {lg}. Son bir yılda {tr(v["comm"])} commit. Son 30 günde {v["pushes"]} push, '
            f'zirve saat {peak:02d}:00, en yoğun gün {GUN[wpeak]}.">{"".join(o)}</svg>\n')


def main():
    tok = token()
    if not tok:
        print("METRICS_TOKEN yok — mevcut veri paneli korunuyor"); return
    v = fetch(tok)
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"data-{p['name']}.svg").write_text(build(p, v), encoding="utf-8")
    print(f"veri paneli yazıldı: {v['repos']} depo, diller {[(n, round(s)) for n, s in v['langs']]}, "
          f"{v['pushes']} push/30g, +{tr(v['add'])}/−{tr(v['dele'])} satır, {tr(v['comm'])} commit")


if __name__ == "__main__":
    main()
