#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Çalışma ritmi paneli: saat ve haftanın günü dağılımı.

Veri kaynağı yereldeki git depolarıdır (GitHub'a hiç gitmemiş işler dahil),
bu yüzden CI'da koşmaz — elle yenilenir:  python tools/gen_rhythm.py
Sonuç assets/rhythm-{light,dark}.svg dosyalarına yazılır.
"""
import collections, datetime, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN = pathlib.Path.home() / "birsav"
EMAILS = {"ekinakkaya1@hotmail.com", "ekinakkaya0@hotmail.com",
          "brsvbilisim@gmail.com", "birsavunmasanayi@gmail.com"}
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
GUN = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#8C959F", ok="#1A7F37", track="#E4E8EC", sheen="#0D1117", sheen_a=0.055,
             rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#6E7681", ok="#3FB950", track="#21262D", sheen="#FFFFFF", sheen_a=0.085,
             rim="#FFFFFF", rim_a=0.075)

def scan():
    gits = [p.parent for p in SCAN.glob("*/.git")] + [p.parent for p in SCAN.glob("*/*/.git")]
    hours, wdays = collections.Counter(), collections.Counter()
    repos = total = 0
    for g in gits:
        try:
            out = subprocess.run(["git", "-C", str(g), "log", "--all",
                                  "--pretty=%ae|%ad", "--date=format:%H|%u"],
                                 capture_output=True, text=True, timeout=60).stdout
        except Exception:
            continue
        n = 0
        for line in out.splitlines():
            parts = line.split("|")
            if len(parts) != 3:
                continue
            ae, h, d = parts
            if ae.strip().lower() not in EMAILS:
                continue
            try:
                hours[int(h)] += 1; wdays[int(d)] += 1; n += 1
            except ValueError:
                pass
        if n:
            repos += 1; total += n
    if not total:
        sys.exit("commit bulunamadı — SCAN yolu ya da EMAILS listesi yanlış olabilir")
    return hours, wdays, repos, total

def tr(n):
    return f"{n:,}".replace(",", ".")

def build(p, hours, wdays, repos, total, stamp):
    W, H = 1000, 208
    CYC, FILL, HOLD = 17.0, 6.0, 8.0
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')

    def bars(x0, x1, labels, vals, title, idx0):
        out = [f'<text x="{x0}" y="27" font-family="{MONO}" font-size="9.5" letter-spacing="2" fill="{p["faint"]}">{title}</text>']
        n = len(vals); mx = max(vals) or 1
        span = (x1 - x0) / n
        bw = span * 0.66
        BASE, MAXH = 152, 104
        peak = vals.index(mx)
        for i, v in enumerate(vals):
            h = max(1.5, MAXH * v / mx)
            x = x0 + i*span + (span-bw)/2
            t = FILL * ((idx0 + i) / 30.0)
            k1 = round(t/CYC, 5); k2 = round((t+1.1)/CYC, 5)
            k3 = round((FILL+HOLD)/CYC, 5); k4 = round((FILL+HOLD+0.7)/CYC, 5)
            col = p["ok"] if i == peak else p["track"]
            out.append(f'<rect x="{x:.1f}" y="{BASE}" width="{bw:.1f}" height="0" rx="2" fill="{col}">'
                       f'<animate attributeName="height" values="0;0;{h:.1f};{h:.1f};0;0" '
                       f'keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="y" values="{BASE};{BASE};{BASE-h:.1f};{BASE-h:.1f};{BASE};{BASE}" '
                       f'keyTimes="0;{k1};{k2};{k3};{k4};1" dur="{CYC}s" repeatCount="indefinite"/>'
                       f'<title>{labels[i]}: {tr(v)} commit</title></rect>')
            if labels[i] is not None and (n == 7 or i % 3 == 0):
                out.append(f'<text x="{x+bw/2:.1f}" y="{BASE+15}" text-anchor="middle" '
                           f'font-family="{MONO}" font-size="9" fill="{p["faint"]}">{labels[i]}</text>')
        out.append(f'<line x1="{x0}" y1="{BASE+1}" x2="{x1}" y2="{BASE+1}" stroke="{p["edge"]}"/>')
        return "".join(out)

    hv = [hours.get(h, 0) for h in range(24)]
    wv = [wdays.get(d, 0) for d in range(1, 8)]
    o.append(bars(28, 668, [f"{h:02d}" for h in range(24)], hv, "ÇALIŞMA SAATİ", 0))
    o.append(bars(716, 972, GUN, wv, "HAFTANIN GÜNÜ", 24))
    o.append(f'<line x1="692" y1="20" x2="692" y2="{H-26}" stroke="{p["edge"]}"/>')

    gece = sum(hours.get(h, 0) for h in (22, 23, 0, 1, 2, 3))
    pay = round(100 * gece / total)
    zirve = max(range(24), key=lambda h: hours.get(h, 0))
    o.append(f'<text x="28" y="{H-12}" font-family="{MONO}" font-size="9.5" fill="{p["faint"]}">'
             f'{repos} depo · {tr(total)} commit · zirve {zirve:02d}:00 · gece 22-03 arası %{pay} · yerel git geçmişi, {stamp}</text>')

    o.append(f'<g clip-path="url(#cprh)"><rect x="-420" y="-{H}" width="300" height="{H*3}" '
             f'fill="url(#swrh)" transform="skewX(-16)">'
             f'<animate attributeName="x" values="-420;-420;{W+260};{W+260}" '
             f'keyTimes="0;0.25;0.72;1" dur="19s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')

    defs = (f'<clipPath id="cprh"><rect width="{W}" height="{H}" rx="6"/></clipPath>'
            f'<linearGradient id="swrh" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{p["sheen"]}" stop-opacity="0"/>'
            f'<stop offset="45%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="55%" stop-color="{p["sheen"]}" stop-opacity="{p["sheen_a"]}"/>'
            f'<stop offset="100%" stop-color="{p["sheen"]}" stop-opacity="0"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Çalışma ritmi: {repos} depoda {tr(total)} commit, '
            f'zirve saat {zirve:02d}:00, gecenin payı yüzde {pay}">'
            f'<defs>{defs}</defs>{"".join(o)}</svg>\n')

def main():
    hours, wdays, repos, total = scan()
    stamp = datetime.date.today().strftime("%d.%m.%Y")
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"rhythm-{p['name']}.svg").write_text(
            build(p, hours, wdays, repos, total, stamp), encoding="utf-8")
    print(f"çalışma ritmi yazıldı: {repos} depo, {tr(total)} commit, zirve "
          f"{max(range(24), key=lambda h: hours.get(h,0)):02d}:00")

if __name__ == "__main__":
    main()
