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

LIGHT = dict(name="light", card="#F6F8FA", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", sheen="#0D1117", sheen_a=0.055, rim=None, rim_a=0,
             snake="#116329", shade="#0B1620", lv=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"])
DARK  = dict(name="dark", card="#0E141B", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
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
ISO_Y    = 128                # yoğunluk taban satırı (r=0)
ISO_PY   = 11.6
ISO_SK   = 5.2
ISO_TW   = 15.0
RISE     = [0, 6, 12, 19, 27]
LS_TOP   = 246
H        = 360
BASE     = H - 14             # manzara taban çizgisi


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
             f'fill="{p["ok"]}" opacity="0.28"/>')


    # ── başlık şeridi ────────────────────────────────────────────────────
    o.append(f'<text x="{CX0}" y="34" font-family="{MONO}" font-size="9.5" letter-spacing="2.4" '
             f'fill="{p["faint"]}">SON BİR YIL</text>')
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

    # ── yoğunluk: oblik çubuklar, yılanla aynı sütunda parlar ────────────
    o.append(f'<text x="{CX0}" y="{ISO_Y-46}" font-family="{MONO}" font-size="9.5" letter-spacing="2.4" '
             f'fill="{p["faint"]}">YOĞUNLUK</text>')
    o.append(f'<text x="{CX1}" y="{ISO_Y-46}" text-anchor="end" font-family="{MONO}" font-size="8.5" '
             f'letter-spacing="1.2" fill="{p["faint"]}">her çubuk bir gün</text>')
    for wi, wk in enumerate(weeks):
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

    for li, (vals, amp, op) in enumerate(
            ((smooth(12), 96, 0.26), (smooth(6), 74, 0.44), (smooth(2), 52, 0.86))):
        pt = profile(vals, amp)
        col = mix(p["ok"], p["card"], 0.46 - li*0.23)
        o.append(f'<g clip-path="url(#lsclip)" fill="{col}" opacity="{op}">'
                 f'<path d="{ridge(pt)}"/></g>')
    o.append(f'<line x1="0" y1="{BASE}" x2="{W}" y2="{BASE}" stroke="{p["edge"]}"/>')
    o.append(f'<text x="{CX0}" y="{LS_TOP-14}" font-family="{MONO}" font-size="11.5" '
             f'letter-spacing="2.4" fill="{p["faint"]}">github.com/ekinakkaya0</text>')

    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="none" stroke="{p["edge"]}"/>')

    defs = (f'<clipPath id="panel"><rect width="{W}" height="{H}" rx="8"/></clipPath>'
            f'<clipPath id="lsclip"><rect x="1" y="{LS_TOP-2}" width="{W-2}" height="{H-LS_TOP+1}"/></clipPath>'
            '')

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
