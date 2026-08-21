#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tek parça aktivite paneli: takvim + yılan + yoğunluk + manzara.

Dördü ayrı görsel değil, tek SVG içinde tek zemin, tek kenar, tek ışık
süpürmesi ve ortak bir tarama başlığıyla birbirine bağlı. Yılan da burada
üretilir; üçüncü parti bir servise bağlı değildir.

Veri: https://github.com/users/<login>/contributions — GitHub'ın profil
sayfasında kullandığı genel uç nokta. Token gerektirmez, tam olarak bir
ziyaretçinin gördüğü sayıları verir.
"""
import re, sys, urllib.request, pathlib

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", sheen="#0D1117", sheen_a=0.055, rim=None, rim_a=0,
             snake="#116329", shade="#0B1620", lv=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"])
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#6E7681", ok="#3FB950", sheen="#FFFFFF", sheen_a=0.085, rim="#FFFFFF",
             rim_a=0.075, snake="#56D364", shade="#050A0F", lv=["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"])

AY = ["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"]
GUN = {1: "Pzt", 3: "Çar", 5: "Cum"}

TD  = re.compile(r'<td\b[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>')
TIP = re.compile(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', re.S)
ATTR = lambda tag, name: (re.search(name + r'="([^"]*)"', tag) or [None, None])[1]

# ── geometri ────────────────────────────────────────────────────────────────
W        = 1000
RAIL_X   = 13
CX0, CX1 = 36, 978
GX       = 70                 # ızgara ve yoğunluk bloğu ortak sol kenar
PITCH    = 17
CELL     = 14
HEAD_H   = 54
CAL_Y    = 92                 # ızgara üst kenarı
CAL_H    = 7 * PITCH - (PITCH - CELL)
ISO_Y    = 322                # yoğunluk taban satırı (r=0)
ISO_PY   = 11.6
ISO_SK   = 5.2
ISO_TW   = 15.0
RISE     = [0, 6, 12, 19, 27]
LS_TOP   = 430
H        = 540
BASE     = H - 14             # manzara taban çizgisi
CYCLE    = 34.0               # yılanın bir turu


def tr(n):
    return f"{n:,}".replace(",", ".")


def mix(a, b, t):
    ca = [int(a[i:i+2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(ca[i] + (cb[i]-ca[i])*t) for i in range(3))


def fetch():
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
            "date": date, "weekday": weekday,
            "count": counts.get(did, 0), "level": int(ATTR(tag, "data-level") or 0)})
    if not cols:
        sys.exit("katkı takvimi ayrıştırılamadı — GitHub biçimi değişmiş olabilir")
    return [sorted(cols[k], key=lambda d: d["weekday"]) for k in sorted(cols)]


def streaks(days):
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    tail = days[:-1] if days and days[-1]["count"] == 0 else days
    now = 0
    for d in reversed(tail):
        if d["count"] > 0:
            now += 1
        else:
            break
    return longest, now


def build(p, weeks, total, longest, now):
    days = [d for wk in weeks for d in wk]
    o = []

    # ── zemin, kenar, üst iç ışık ────────────────────────────────────────
    o.append(f'<rect width="{W}" height="{H}" rx="8" fill="{p["card"]}"/>')
    if p["rim"]:
        o.append(f'<path d="M9,1.2 H{W-9}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" '
                 f'stroke-width="1.2" fill="none"/>')

    # ── soldan aşağı inen ortak aksan rayı ───────────────────────────────
    o.append(f'<rect x="{RAIL_X}" y="24" width="3" height="{H-48}" rx="1.5" '
             f'fill="{p["ok"]}" opacity="0.16"/>')
    o.append(f'<rect x="{RAIL_X}" y="24" width="3" height="96" rx="1.5" fill="{p["ok"]}" opacity="0.85">'
             f'<animate attributeName="y" values="24;{H-120}" dur="{CYCLE}s" repeatCount="indefinite"/>'
             f'</rect>')

    # ── başlık şeridi ────────────────────────────────────────────────────
    o.append(f'<text x="{CX0}" y="34" font-family="{MONO}" font-size="9.5" letter-spacing="2.4" '
             f'fill="{p["faint"]}">AKTİVİTE</text>')
    stats = [(tr(total), "katkı"), (f"{tr(longest)} gün", "en uzun seri"), (f"{tr(now)} gün", "güncel seri")]
    LW, VW, GAP, PAD = 6.65, 8.5, 9.0, 30.0   # etiket/değer karakter genişliği ve boşluklar
    x = CX1
    for val, lab in reversed(stats):
        o.append(f'<text x="{x:.1f}" y="34" text-anchor="end" font-family="{MONO}" font-size="10" '
                 f'letter-spacing="1.1" fill="{p["faint"]}">{lab}</text>')
        x -= len(lab) * LW + GAP
        o.append(f'<text x="{x:.1f}" y="34" text-anchor="end" font-family="{MONO}" font-size="13" '
                 f'font-weight="700" fill="{p["ink"]}">{val}</text>')
        x -= len(val) * VW + PAD
    o.append(f'<line x1="{CX0}" y1="{HEAD_H}" x2="{CX1}" y2="{HEAD_H}" stroke="{p["edge"]}"/>')

    # ── ay ve gün etiketleri ─────────────────────────────────────────────
    seen = set()
    for wi, wk in enumerate(weeks):
        d0 = wk[0]["date"]; m = int(d0[5:7])
        if m not in seen and int(d0[8:10]) <= 7:
            seen.add(m)
            o.append(f'<text x="{GX+wi*PITCH}" y="{CAL_Y-9}" font-family="{MONO}" font-size="9" '
                     f'fill="{p["faint"]}">{AY[m-1]}</text>')
    for wd, lab in GUN.items():
        o.append(f'<text x="{GX-9}" y="{CAL_Y+wd*PITCH+11}" text-anchor="end" font-family="{MONO}" '
                 f'font-size="8.5" fill="{p["faint"]}">{lab}</text>')

    # ── yılanın gezeceği yol: sütun sütun, aşağı-yukarı ──────────────────
    order, pts = [], []
    for wi, wk in enumerate(weeks):
        seq = wk if wi % 2 == 0 else list(reversed(wk))
        for d in seq:
            cx = GX + wi*PITCH + CELL/2
            cy = CAL_Y + d["weekday"]*PITCH + CELL/2
            order.append((wi, d)); pts.append((cx, cy))
    N = len(order)

    # ── takvim hücreleri; yılan geçince boşalır ──────────────────────────
    for k, (wi, d) in enumerate(order):
        lv = min(4, max(0, d["level"]))
        x = GX + wi*PITCH; y = CAL_Y + d["weekday"]*PITCH
        cell = (f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{p["lv"][lv]}">'
                f'<title>{d["date"]}: {d["count"]}</title>')
        if lv:
            t = round(k / max(1, N-1), 5)
            cell += (f'<animate attributeName="fill" '
                     f'values="{p["lv"][lv]};{p["lv"][lv]};{p["lv"][0]};{p["lv"][0]}" '
                     f'keyTimes="0;{max(0.0, t-0.0012)};{t};1" dur="{CYCLE}s" '
                     f'repeatCount="indefinite" calcMode="discrete"/>')
        o.append(cell + '</rect>')

    # ── yılan: baş + gövde, aynı yolda gecikmeli ─────────────────────────
    SEG = 7
    for i in range(SEG):
        sz = CELL - i*1.35
        op = 0.95 - i*0.105
        col = p["snake"] if i == 0 else mix(p["snake"], p["card"], 0.12 + i*0.085)
        xs = ";".join(f"{x - sz/2:.1f}" for x, _ in pts)
        ys = ";".join(f"{y - sz/2:.1f}" for _, y in pts)
        o.append(f'<rect x="{pts[0][0]-sz/2:.1f}" y="{pts[0][1]-sz/2:.1f}" width="{sz:.2f}" '
                 f'height="{sz:.2f}" rx="{sz/3:.2f}" fill="{col}" opacity="{op:.2f}">'
                 f'<animate attributeName="x" values="{xs}" dur="{CYCLE}s" '
                 f'repeatCount="indefinite" begin="-{i*0.30:.2f}s"/>'
                 f'<animate attributeName="y" values="{ys}" dur="{CYCLE}s" '
                 f'repeatCount="indefinite" begin="-{i*0.30:.2f}s"/></rect>')

    # ── gösterge ─────────────────────────────────────────────────────────
    ly = CAL_Y + CAL_H + 26
    o.append(f'<text x="{GX}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{p["faint"]}">az</text>')
    for i, c in enumerate(p["lv"]):
        o.append(f'<rect x="{GX+24+i*15}" y="{ly-9}" width="11" height="11" rx="2.5" fill="{c}"/>')
    o.append(f'<text x="{GX+24+len(p["lv"])*15+6}" y="{ly}" font-family="{MONO}" font-size="8.5" '
             f'fill="{p["faint"]}">çok</text>')
    o.append(f'<text x="{CX1}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="8.5" '
             f'letter-spacing="1.2" fill="{p["faint"]}">yılan bir yılı baştan sona tarıyor</text>')
    o.append(f'<line x1="{CX0}" y1="{ly+18}" x2="{CX1}" y2="{ly+18}" stroke="{p["edge"]}"/>')

    # ── yoğunluk: oblik çubuklar, yılanla aynı sütunda parlar ────────────
    o.append(f'<text x="{CX0}" y="{ISO_Y-46}" font-family="{MONO}" font-size="9.5" letter-spacing="2.4" '
             f'fill="{p["faint"]}">YOĞUNLUK</text>')
    o.append(f'<text x="{CX1}" y="{ISO_Y-46}" text-anchor="end" font-family="{MONO}" font-size="8.5" '
             f'letter-spacing="1.2" fill="{p["faint"]}">her çubuk bir gün</text>')
    for wi, wk in enumerate(weeks):
        t = round((wi * 7) / max(1, N-1), 5)
        a = max(0.0, t - 0.0015); b = min(1.0, t + 0.035)
        o.append(f'<g opacity="0.5"><animate attributeName="opacity" '
                 f'values="0.5;0.5;1;0.5;0.5" keyTimes="0;{a};{t};{b};1" '
                 f'dur="{CYCLE}s" repeatCount="indefinite"/>')
        for d in wk:
            r = d["weekday"]; lv = min(4, max(0, d["level"])); h = RISE[lv]
            bx = GX + wi*PITCH - r*ISO_SK; by = ISO_Y + r*ISO_PY
            top = p["lv"][lv]
            front = mix(top, p["shade"], 0.34)   # gölge her temada koyuya gider
            side = mix(top, p["shade"], 0.17)
            if h:
                o.append(f'<path d="M{bx-ISO_SK:.1f},{by+ISO_PY-h:.1f} L{bx-ISO_SK+ISO_TW:.1f},{by+ISO_PY-h:.1f} '
                         f'L{bx-ISO_SK+ISO_TW:.1f},{by+ISO_PY:.1f} L{bx-ISO_SK:.1f},{by+ISO_PY:.1f} Z" fill="{front}"/>')
                o.append(f'<path d="M{bx+ISO_TW:.1f},{by-h:.1f} L{bx-ISO_SK+ISO_TW:.1f},{by+ISO_PY-h:.1f} '
                         f'L{bx-ISO_SK+ISO_TW:.1f},{by+ISO_PY:.1f} L{bx+ISO_TW:.1f},{by:.1f} Z" fill="{side}"/>')
            o.append(f'<path d="M{bx:.1f},{by-h:.1f} L{bx+ISO_TW:.1f},{by-h:.1f} '
                     f'L{bx-ISO_SK+ISO_TW:.1f},{by+ISO_PY-h:.1f} L{bx-ISO_SK:.1f},{by+ISO_PY-h:.1f} Z" fill="{top}">'
                     f'<title>{d["date"]}: {d["count"]}</title></path>')
        o.append('</g>')

    # ── iki bloğu birbirine bağlayan ortak tarama başlığı ────────────────
    x0 = GX + CELL/2; x1 = GX + (len(weeks)-1)*PITCH + CELL/2
    o.append(f'<rect x="{x0}" y="{CAL_Y-4}" width="1.5" height="{ISO_Y + 6*ISO_PY + 14 - CAL_Y}" '
             f'fill="{p["ok"]}" opacity="0.30">'
             f'<animate attributeName="x" values="{x0};{x1}" dur="{CYCLE}s" repeatCount="indefinite"/></rect>')
    o.append(f'<line x1="{CX0}" y1="{LS_TOP-38}" x2="{CX1}" y2="{LS_TOP-38}" stroke="{p["edge"]}"/>')

    # ── manzara: katkı yoğunluğundan türetilmiş, kayan katmanlar ─────────
    counts = [d["count"] for d in days]
    srt = sorted(counts); cap = max(1, srt[int(len(srt)*0.96)] if srt else 1)

    def smooth(k):
        return [sum(counts[max(0, i-k):min(len(counts), i+k+1)]) /
                (min(len(counts), i+k+1) - max(0, i-k)) for i in range(len(counts))]

    def profile(vals, amp):
        m = max(vals) or 1
        return [(i * (W / (len(vals)-1)),
                 BASE - (0.035 + 0.965 * min(1.0, v / max(m, cap*0.5))) * amp)
                for i, v in enumerate(vals)]

    def ridge(pt, dx=0.0):
        d = f"M{pt[0][0]+dx:.1f},{BASE:.1f} L{pt[0][0]+dx:.1f},{pt[0][1]:.1f}"
        for x, y in pt[1:]:
            d += f" L{x+dx:.1f},{y:.1f}"
        return d + f" L{pt[-1][0]+dx:.1f},{BASE:.1f} Z"

    for li, (vals, amp, op, dur) in enumerate(
            ((smooth(12), 96, 0.26, 96.0), (smooth(6), 74, 0.44, 74.0), (smooth(2), 52, 0.86, 56.0))):
        pt = profile(vals, amp)
        col = mix(p["ok"], p["card"], 0.46 - li*0.23)
        o.append(f'<g clip-path="url(#lsclip)" fill="{col}" opacity="{op}"><g>'
                 f'<animateTransform attributeName="transform" type="translate" '
                 f'values="0 0;-{W} 0" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<path d="{ridge(pt)}"/><path d="{ridge(pt, W)}"/></g></g>')
    o.append(f'<line x1="0" y1="{BASE}" x2="{W}" y2="{BASE}" stroke="{p["edge"]}"/>')
    o.append(f'<text x="{CX0}" y="{LS_TOP-14}" font-family="{MONO}" font-size="11.5" '
             f'letter-spacing="2.4" fill="{p["faint"]}">github.com/ekinakkaya0</text>')

    # ── panel boyunca tek ışık süpürmesi ─────────────────────────────────
    o.append(f'<g clip-path="url(#panel)"><rect x="-460" y="-{H}" width="330" height="{H*3}" '
             f'fill="url(#sheen)" transform="skewX(-16)">'
             f'<animate attributeName="x" values="-460;-460;{W+300};{W+300}" '
             f'keyTimes="0;0.25;0.72;1" dur="23s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="none" stroke="{p["edge"]}"/>')

    defs = (f'<clipPath id="panel"><rect width="{W}" height="{H}" rx="8"/></clipPath>'
            f'<clipPath id="lsclip"><rect x="1" y="{LS_TOP-2}" width="{W-2}" height="{H-LS_TOP+1}"/></clipPath>'
            f'<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{p["sheen"]}" stop-opacity="0"/>'
            f'<stop offset="45%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="55%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="100%" stop-color="{p["sheen"]}" stop-opacity="0"/></linearGradient>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Aktivite: son bir yılda {tr(total)} katkı, en uzun seri {tr(longest)} gün, '
            f'güncel seri {tr(now)} gün">'
            f'<defs>{defs}</defs>{"".join(o)}</svg>\n')


def main():
    weeks = fetch()
    days = sorted((d for wk in weeks for d in wk), key=lambda d: d["date"])
    total = sum(d["count"] for d in days)
    longest, now = streaks(days)
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"activity-{p['name']}.svg").write_text(
            build(p, weeks, total, longest, now), encoding="utf-8")
    print(f"aktivite paneli yazıldı: {tr(total)} katkı, en uzun {longest}, güncel {now}, "
          f"{len(weeks)} hafta")


if __name__ == "__main__":
    main()
