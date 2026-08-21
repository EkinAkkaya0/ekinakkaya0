#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İletişim rozetleri: sayfanın kendi diliyle çizilmiş küçük SVG'ler.

shields.io yerine burada üretiliyor — sayfadaki tek yabancı tipografi oydu.
Her rozet ayrı dosya çünkü her biri ayrı bağlantıya sarılıyor (SVG içindeki
<a> etiketi <img> ile yüklenen SVG'de çalışmaz).
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = json.load(open(pathlib.Path(__file__).resolve().parent / "icons_badge.json"))
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

LIGHT = dict(name="light", chip="#FFFFFF", edge="#D0D7DE", ink="#1F2328", rim=None, rim_a=0)
DARK  = dict(name="dark",  chip="#161B22", edge="#30363D", ink="#E6EDF3", rim="#FFFFFF", rim_a=0.06)

BADGES = [
    ("linkedin", "linkedin", "#0A66C2", "Ekin Doğucan Akkaya"),
    ("mail",     "maildotru", "#8B949E", "ekinakkaya0@hotmail.com"),
]

FS, H, ICO, PAD, GAP = 12.0, 30, 15, 13, 8
CW = FS * 0.6005


def build(p, slug, icon, col, text):
    w = round(PAD*2 + ICO + GAP + len(text)*CW, 1)
    o = [f'<rect x="0.5" y="0.5" width="{w-1:.1f}" height="{H-1}" rx="7" '
         f'fill="{p["chip"]}" stroke="{p["edge"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M8,1.4 H{w-8:.1f}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" '
                 f'stroke-width="1.2" fill="none"/>')
    o.append(f'<g fill="{col}" transform="translate({PAD},{(H-ICO)/2:.1f}) scale({ICO/24:.4f})">'
             f'<path d="{ICONS[icon]}"/></g>')
    o.append(f'<text x="{PAD+ICO+GAP}" y="{H/2+4.2:.1f}" font-family="{MONO}" font-size="{FS}" '
             f'fill="{p["ink"]}">{text}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {H}" '
            f'width="{w:.1f}" height="{H}" role="img" aria-label="{text}">{"".join(o)}</svg>\n')


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    for slug, icon, col, text in BADGES:
        for p in (LIGHT, DARK):
            (ROOT / "assets" / f"badge-{slug}-{p['name']}.svg").write_text(
                build(p, slug, icon, col, text), encoding="utf-8")
    print(f"{len(BADGES)} rozet x 2 tema yazıldı")


if __name__ == "__main__":
    main()
