#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub katkı takvimini sayfanın cam diline uygun SVG olarak üretir.

Veri kaynağı: https://github.com/users/<login>/contributions — GitHub'ın profil
sayfasında kullandığı genel uç nokta. Token gerektirmez ve tam olarak bir
ziyaretçinin gördüğü sayıları verir. (GraphQL denendi ve bırakıldı: Actions'ın
GITHUB_TOKEN'ı uygulama kimliğiyle sorguladığı için katkıları eksik sayıyor —
ölçüldü, 36'ya karşı 42.)

Her gün GitHub Actions ile koşar; assets/contrib-{light,dark}.svg yazar.
"""
import re, sys, urllib.request, pathlib

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", sheen="#0D1117", sheen_a=0.055, rim=None, rim_a=0,
             lv=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"])
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#6E7681", ok="#3FB950", sheen="#FFFFFF", sheen_a=0.085, rim="#FFFFFF", rim_a=0.075,
             lv=["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"])

AY = ["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"]

TD  = re.compile(r'<td\b[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>')
TIP = re.compile(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', re.S)
ATTR = lambda tag, name: (re.search(name + r'="([^"]*)"', tag) or [None, None])[1]

def fetch():
    """Genel katkı takvimini çeker; (haftalar, toplam) döndürür."""
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        html = r.read().decode("utf-8", "replace")

    counts = {}
    for tid, text in TIP.findall(html):
        m = re.search(r"([\d,]+)\s+contribution", text)
        counts[tid] = int(m.group(1).replace(",", "")) if m else 0

    cols = {}
    for tag in TD.findall(html):
        date = ATTR(tag, "data-date")
        if not date:
            continue
        did = ATTR(tag, "id") or ""
        m = re.match(r"contribution-day-component-(\d+)-(\d+)$", did)
        weekday, week = (int(m.group(1)), int(m.group(2))) if m else (0, len(cols))
        cols.setdefault(week, []).append({
            "date": date,
            "weekday": weekday,
            "contributionCount": counts.get(did, 0),
            "level": int(ATTR(tag, "data-level") or 0),
        })

    if not cols:
        sys.exit("katkı takvimi ayrıştırılamadı — GitHub biçimi değişmiş olabilir")
    weeks = [{"contributionDays": cols[k]} for k in sorted(cols)]
    total = sum(d["contributionCount"] for w in weeks for d in w["contributionDays"])
    return {"weeks": weeks, "totalContributions": total}

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


def mix(hexa, hexb, t):
    """iki rengi t oranında karıştır (t=0 -> a, t=1 -> b)"""
    a = [int(hexa[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(hexb[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))


def glass_defs(p, uid, W, H):
    return (f'<clipPath id="cp{uid}"><rect width="{W}" height="{H}" rx="6"/></clipPath>'
            f'<linearGradient id="sw{uid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{p["sheen"]}" stop-opacity="0"/>'
            f'<stop offset="45%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="55%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="100%" stop-color="{p["sheen"]}" stop-opacity="0"/></linearGradient>')


def glass_sweep(p, uid, W, H, dur):
    return (f'<g clip-path="url(#cp{uid})"><rect x="-420" y="-{H}" width="300" height="{H*3}" '
            f'fill="url(#sw{uid})" transform="skewX(-16)">'
            f'<animate attributeName="x" values="-420;-420;{W+260};{W+260}" '
            f'keyTimes="0;0.25;0.72;1" dur="{dur}s" repeatCount="indefinite"/></rect></g>')


def build_iso(p, weeks, total):
    """Oblik (2.5B) takvim: her günün yüksekliği o günkü katkı yoğunluğu."""
    W, H = 1000, 182
    PX, SK, PY = 17, 5.2, 11.6
    TW = 15.0
    OX, OY = 52, 60
    RISE = [0, 6, 12, 19, 27]
    REPLAY, HOLD, CYC = 9.0, 7.0, 17.0
    n = len(weeks)
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    o.append(f'<text x="22" y="27" font-family="{MONO}" font-size="9.5" letter-spacing="2" fill="{p["faint"]}">YOĞUNLUK</text>')
    o.append(f'<text x="{W-22}" y="27" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.2" fill="{p["faint"]}">her çubuk bir gün</text>')

    for wi, wk in enumerate(weeks):
        t = REPLAY * (wi / max(1, n - 1))
        lit = round(t / CYC, 5)
        dim = round((REPLAY + HOLD) / CYC, 5)
        end = round((REPLAY + HOLD + 0.6) / CYC, 5)
        anim = (f'<animate attributeName="opacity" values="0.55;0.55;1;1;0.55;0.55" '
                f'keyTimes="0;{max(0.0, lit-0.004)};{lit};{dim};{end};1" '
                f'dur="{CYC}s" repeatCount="indefinite"/>')
        o.append(f'<g opacity="0.55">{anim}')
        for day in wk["contributionDays"]:
            r = day["weekday"]; lv = min(4, max(0, day["level"])); h = RISE[lv]
            bx = OX + wi*PX - r*SK; by = OY + r*PY
            top = p["lv"][lv]
            front = mix(top, p["card"], 0.42)
            side = mix(top, p["card"], 0.24)
            g = []
            if h:
                g.append(f'<path d="M{bx-SK:.1f},{by+PY-h:.1f} L{bx-SK+TW:.1f},{by+PY-h:.1f} '
                         f'L{bx-SK+TW:.1f},{by+PY:.1f} L{bx-SK:.1f},{by+PY:.1f} Z" fill="{front}"/>')
                g.append(f'<path d="M{bx+TW:.1f},{by-h:.1f} L{bx-SK+TW:.1f},{by+PY-h:.1f} '
                         f'L{bx-SK+TW:.1f},{by+PY:.1f} L{bx+TW:.1f},{by:.1f} Z" fill="{side}"/>')
            g.append(f'<path d="M{bx:.1f},{by-h:.1f} L{bx+TW:.1f},{by-h:.1f} '
                     f'L{bx-SK+TW:.1f},{by+PY-h:.1f} L{bx-SK:.1f},{by+PY-h:.1f} Z" fill="{top}">'
                     f'<title>{day["date"]}: {day["contributionCount"]}</title></path>')
            o.append("".join(g))
        o.append('</g>')

    o.append(glass_sweep(p, "iso", W, H, 21))
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Günlük katkı yoğunluğunun üç boyutlu görünümü">'
            f'<defs>{glass_defs(p, "iso", W, H)}</defs>{"".join(o)}</svg>\n')


def build_landscape(p, days):
    """Katkıları arazi yüksekliği gibi okuyup katmanlı bir manzara çizer."""
    W, H = 1000, 150
    counts = [d["contributionCount"] for d in days]
    srt = sorted(counts)
    cap = max(1, srt[int(len(srt)*0.96)] if srt else 1)

    def smooth(k):
        out = []
        for i in range(len(counts)):
            lo, hi = max(0, i-k), min(len(counts), i+k+1)
            out.append(sum(counts[lo:hi]) / (hi-lo))
        return out

    def layer(vals, amp, base):
        m = max(vals) or 1
        pts = []
        for i, v in enumerate(vals):
            x = i * (W / (len(vals)-1))
            y = base - (0.07 + 0.93 * min(1.0, v/max(m, cap*0.5))) * amp
            pts.append((x, y))
        return pts

    def path(pts, base, dx=0.0):
        d = f"M{pts[0][0]+dx:.1f},{base:.1f} L{pts[0][0]+dx:.1f},{pts[0][1]:.1f}"
        for x, y in pts[1:]:
            d += f" L{x+dx:.1f},{y:.1f}"
        d += f" L{pts[-1][0]+dx:.1f},{base:.1f} Z"
        return d

    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    BASE = H - 12
    specs = ((smooth(12), 100, 0.28, 96.0), (smooth(6), 78, 0.46, 74.0), (smooth(2), 58, 0.88, 56.0))
    for li, (vals, amp, op, dur) in enumerate(specs):
        pts = layer(vals, amp, BASE)
        col = mix(p["ok"], p["card"], 0.46 - li*0.23)
        o.append(f'<g clip-path="url(#cpls)" fill="{col}" opacity="{op}">'
                 f'<g><animateTransform attributeName="transform" type="translate" '
                 f'values="0 0;-{W} 0" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<path d="{path(pts, BASE)}"/><path d="{path(pts, BASE, W)}"/></g></g>')
    o.append(f'<line x1="0" y1="{BASE}" x2="{W}" y2="{BASE}" stroke="{p["edge"]}"/>')
    o.append(f'<text x="24" y="26" font-family="{MONO}" font-size="11.5" '
             f'letter-spacing="2.2" fill="{p["faint"]}">github.com/ekinakkaya0</text>')
    o.append(glass_sweep(p, "ls", W, H, 27))
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Katkı yoğunluğundan türetilmiş manzara">'
            f'<defs>{glass_defs(p, "ls", W, H)}'
            f'<clipPath id="cpls"><rect width="{W}" height="{H}" rx="6"/></clipPath></defs>{"".join(o)}</svg>\n')


def tr(n):
    """Türkçe binlik ayracı: 5873 -> 5.873"""
    return f"{n:,}".replace(",", ".")

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
    # yılın hızlandırılmış tekrarı: hücreler tarih sırasıyla parlar, sonra tam kalır
    REPLAY, HOLD, CYC = 9.0, 7.0, 17.0
    n = len(weeks)
    for wi, wk in enumerate(weeks):
        t = REPLAY * (wi / max(1, n - 1))
        lit = round(t / CYC, 5)
        dim = round((REPLAY + HOLD) / CYC, 5)
        end = round((REPLAY + HOLD + 0.6) / CYC, 5)
        # tüm haftayı tek <g> altında sür: 7 animasyon yerine 1
        o.append(f'<g opacity="0.55"><animate attributeName="opacity" values="0.55;0.55;1;1;0.55;0.55" '
                 f'keyTimes="0;{max(0.0, lit-0.004)};{lit};{dim};{end};1" '
                 f'dur="{CYC}s" repeatCount="indefinite"/>')
        for day in wk["contributionDays"]:
            lv = min(4, max(0, day["level"]))
            x = GX + wi*PITCH; y = GY + day["weekday"]*PITCH
            o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{p["lv"][lv]}">'
                     f'<title>{day["date"]}: {day["contributionCount"]}</title></rect>')
        o.append('</g>')
    # oynatma başlığı
    o.append(f'<rect x="{GX}" y="{GY-3}" width="2.5" height="{7*PITCH-2}" rx="1.25" fill="{p["ok"]}" opacity="0">'
             f'<animate attributeName="x" values="{GX};{GX};{GX+(n-1)*PITCH};{GX+(n-1)*PITCH}" '
             f'keyTimes="0;0.001;{round(REPLAY/CYC,5)};1" dur="{CYC}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0.9;0.9;0;0" '
             f'keyTimes="0;0.01;{round(REPLAY/CYC,5)};{round((REPLAY+0.4)/CYC,5)};1" dur="{CYC}s" repeatCount="indefinite"/></rect>')

    # gösterge
    ly = GY + 7*PITCH + 14
    o.append(f'<text x="{GX}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">az</text>')
    for i, c in enumerate(p["lv"]):
        o.append(f'<rect x="{GX+24+i*14}" y="{ly-8}" width="10" height="10" rx="2" fill="{c}"/>')
    o.append(f'<text x="{GX+24+len(p["lv"])*14+6}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">çok</text>')

    # sayaçlar
    SX = 790
    o.append(f'<line x1="{SX-24}" y1="24" x2="{SX-24}" y2="{H-24}" stroke="{p["edge"]}"/>')
    for i, (val, lab) in enumerate(((tr(total), "son 1 yıl"),
                                    (tr(longest) + " gün", "en uzun seri"),
                                    (tr(now) + " gün", "güncel seri"))):
        y = 52 + i*40
        o.append(f'<text x="{SX}" y="{y}" font-family="{MONO}" font-size="19" font-weight="700" fill="{p["ink"]}">{val}</text>')
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
            f'role="img" aria-label="Son bir yılda {tr(total)} katkı, en uzun seri {tr(longest)} gün, güncel seri {tr(now)} gün">'
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
        (ROOT / "assets" / f"iso-{p['name']}.svg").write_text(build_iso(p, cal["weeks"], total), encoding="utf-8")
        (ROOT / "assets" / f"landscape-{p['name']}.svg").write_text(build_landscape(p, days), encoding="utf-8")
    print(f"katkı takvimi yazıldı: toplam={total} en_uzun={longest} güncel={now} hafta={len(cal['weeks'])}")

if __name__ == "__main__":
    main()
