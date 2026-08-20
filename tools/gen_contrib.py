#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub katkı takvimini sayfanın cam diline uygun SVG olarak üretir.
Her gün GitHub Actions ile yeniden koşar; assets/contrib-{light,dark}.svg yazar.
Token: GH_TOKEN ortam değişkeni, yoksa `gh auth token`."""
import json, os, subprocess, sys, urllib.request, pathlib, datetime

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", sheen="#0D1117", sheen_a=0.055, rim=None, rim_a=0,
             lv=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"])
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#6E7681", ok="#3FB950", sheen="#FFFFFF", sheen_a=0.085, rim="#FFFFFF", rim_a=0.075,
             lv=["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"])

AY = ["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"]

def token():
    t = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if t: return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

def fetch():
    q = """query($login:String!){ user(login:$login){ contributionsCollection{
      contributionCalendar{ totalContributions
        weeks{ contributionDays{ date weekday contributionCount contributionLevel } } } } } }"""
    body = json.dumps({"query": q, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json",
                 "User-Agent": "contrib-svg"})
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.load(r)
    if "errors" in d: sys.exit("GraphQL hatası: " + json.dumps(d["errors"])[:400])
    return d["data"]["user"]["contributionsCollection"]["contributionCalendar"]

LEVELS = {"NONE":0, "FIRST_QUARTILE":1, "SECOND_QUARTILE":2, "THIRD_QUARTILE":3, "FOURTH_QUARTILE":4}

def streaks(days):
    """en uzun ve güncel seri (bugün boşsa dünden geriye bakar)."""
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, cur)
    tail = days[:]
    if tail and tail[-1]["contributionCount"] == 0: tail = tail[:-1]
    now = 0
    for d in reversed(tail):
        if d["contributionCount"] > 0: now += 1
        else: break
    return longest, now

def build(p, cal, days, total, longest, now):
    W, H = 1000, 176
    CELL, GAP = 11, 2
    PITCH = CELL + GAP
    GX, GY = 78, 46
    weeks = cal["weeks"]
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    o.append(f'<text x="22" y="27" font-family="{MONO}" font-size="9.5" letter-spacing="2" fill="{p["faint"]}">KATKI TAKVİMİ</text>')

    # ay etiketleri
    seen = set()
    for wi, wk in enumerate(weeks):
        d0 = wk["contributionDays"][0]["date"]
        m = int(d0[5:7])
        if m not in seen and int(d0[8:10]) <= 7:
            seen.add(m)
            o.append(f'<text x="{GX+wi*PITCH}" y="{GY-8}" font-family="{MONO}" font-size="9" fill="{p["faint"]}">{AY[m-1]}</text>')

    # gün etiketleri
    for wd, lab in ((1,"Pzt"), (3,"Çar"), (5,"Cum")):
        o.append(f'<text x="{GX-8}" y="{GY+wd*PITCH+9}" text-anchor="end" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">{lab}</text>')

    # hücreler — sütun sütun dalga hâlinde parlıyor
    n = len(weeks)
    for wi, wk in enumerate(weeks):
        ph = round(wi / max(1, n), 4)
        for day in wk["contributionDays"]:
            lv = LEVELS.get(day["contributionLevel"], 0)
            x = GX + wi*PITCH; y = GY + day["weekday"]*PITCH
            a = round(max(0.0, ph-0.02), 4); b = round(min(1.0, ph+0.06), 4)
            o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{p["lv"][lv]}" opacity="0.78">'
                     f'<animate attributeName="opacity" values="0.78;0.78;1;0.78;0.78" '
                     f'keyTimes="0;{a};{ph};{b};1" dur="9s" repeatCount="indefinite"/>'
                     f'<title>{day["date"]}: {day["contributionCount"]}</title></rect>')

    # gösterge
    ly = GY + 7*PITCH + 14
    o.append(f'<text x="{GX}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">az</text>')
    for i, c in enumerate(p["lv"]):
        o.append(f'<rect x="{GX+24+i*14}" y="{ly-8}" width="10" height="10" rx="2" fill="{c}"/>')
    o.append(f'<text x="{GX+24+len(p["lv"])*14+6}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">çok</text>')

    # sayaçlar
    SX = 790
    o.append(f'<line x1="{SX-24}" y1="24" x2="{SX-24}" y2="{H-24}" stroke="{p["edge"]}"/>')
    for i, (val, lab) in enumerate(((total, "son 1 yıl"), (longest, "en uzun seri"), (now, "güncel seri"))):
        y = 52 + i*40
        o.append(f'<text x="{SX}" y="{y}" font-family="{MONO}" font-size="20" font-weight="700" fill="{p["ink"]}">{val}</text>')
        o.append(f'<text x="{SX+2}" y="{y+16}" font-family="{MONO}" font-size="9.5" letter-spacing="1.1" fill="{p["faint"]}">{lab}</text>')

    # cam süpürmesi
    o.append(f'<g clip-path="url(#cpct)"><rect x="-420" y="-{H}" width="300" height="{H*3}" fill="url(#swct)" transform="skewX(-16)">'
             f'<animate attributeName="x" values="-420;-420;{W+260};{W+260}" keyTimes="0;0.25;0.72;1" dur="25s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')

    defs = (f'<clipPath id="cpct"><rect width="{W}" height="{H}" rx="6"/></clipPath>'
            f'<linearGradient id="swct" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{p["sheen"]}" stop-opacity="0"/>'
            f'<stop offset="45%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="55%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="100%" stop-color="{p["sheen"]}" stop-opacity="0"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Son bir yılda {total} katkı, en uzun seri {longest} gün, güncel seri {now} gün">'
            f'<defs>{defs}</defs>{"".join(o)}</svg>\n')

def main():
    cal = fetch()
    days = [d for wk in cal["weeks"] for d in wk["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    total = cal["totalContributions"]
    longest, now = streaks(days)
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"contrib-{p['name']}.svg").write_text(build(p, cal, days, total, longest, now), encoding="utf-8")
    print(f"katkı takvimi yazıldı: toplam={total} en_uzun={longest} güncel={now} hafta={len(cal['weeks'])}")

if __name__ == "__main__":
    main()
