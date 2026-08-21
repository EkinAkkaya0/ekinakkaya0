#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İletişim rozetleri: sayfanın kendi diliyle çizilmiş küçük SVG'ler.

Neden shields.io / komarev değil: onların yüksekliği (20px), köşe yarıçapı
ve tipografisi sabit; sayfadaki diğer rozetlerle aynı düzleme oturmuyorlardı.

Görüntülenme sayısı komarev'den okunup rozete gömülür. Sayaç canlı kalsın
diye README'de 1x1 boyutunda komarev görseli yüklenmeye devam eder —
ziyaretçi o görseli çekmezse komarev saymaz. Bu script'in kendi çekimi
sayacı günde 1 artırır, ihmal edilebilir.

Her rozet ayrı dosyadır çünkü her biri ayrı bağlantıya sarılır: <img> ile
yüklenen bir SVG'nin içindeki <a> etiketi çalışmaz.
"""
import json, pathlib, re, urllib.request

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = json.load(open(pathlib.Path(__file__).resolve().parent / "icons_badge.json"))
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

LIGHT = dict(name="light", chip="#FFFFFF", edge="#D0D7DE", ink="#1F2328",
             faint="#6E7781", rim=None, rim_a=0)
DARK  = dict(name="dark",  chip="#161B22", edge="#30363D", ink="#E6EDF3",
             faint="#8B949E", rim="#FFFFFF", rim_a=0.06)

H, R = 32, 8
FS = 12.0
CW = FS * 0.6005
CELL = 36                 # ikon hücresi
PAD_R = 15                # sağ iç boşluk
GAP = 12                  # ikon hücresi ile metin arası

EYE = ('<path d="M12 5C6.5 5 2.3 8.6 1 12c1.3 3.4 5.5 7 11 7s9.7-3.6 11-7c-1.3-3.4-5.5-7-11-7z'
       'm0 11.5A4.5 4.5 0 1 1 12 7.5a4.5 4.5 0 0 1 0 9zm0-2.2a2.3 2.3 0 1 0 0-4.6 2.3 2.3 0 0 0 0 4.6z"/>')


def views():
    """komarev'den güncel sayıyı oku; erişilemezse rozeti sayısız bas."""
    try:
        req = urllib.request.Request(
            f"https://komarev.com/ghpvc/?username={USER}&style=flat-square",
            headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            svg = r.read().decode("utf-8", "replace")
        m = re.findall(r">\s*([\d,\.]+)\s*</text>", svg)
        return f"{int(m[-1].replace(',', '').replace('.', '')):,}".replace(",", ".") if m else None
    except Exception:
        return None


def chip(p, icon_svg, icon_color, parts):
    """parts: [(metin, renk anahtarı, kalın mı)]"""
    text_w = sum(len(t) for t, _, _ in parts) * CW + (len(parts)-1) * CW
    w = round(CELL + GAP + text_w + PAD_R, 1)
    o = [f'<rect x="0.5" y="0.5" width="{w-1:.1f}" height="{H-1}" rx="{R}" '
         f'fill="{p["chip"]}" stroke="{p["edge"]}"/>',
         f'<path d="M{R},0.5 H{CELL} V{H-0.5} H{R} A{R},{R} 0 0 1 {R-R},{H-0.5-R} '
         f'V{R+0.5} A{R},{R} 0 0 1 {R},0.5 Z" fill="{icon_color}" fill-opacity="0.10"/>',
         f'<line x1="{CELL}" y1="1" x2="{CELL}" y2="{H-1}" stroke="{p["edge"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M{R+2},1.4 H{w-R-2:.1f}" stroke="{p["rim"]}" '
                 f'stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    o.append(f'<g fill="{icon_color}" transform="translate({(CELL-16)/2:.1f},{(H-16)/2:.1f}) '
             f'scale({16/24:.4f})">{icon_svg}</g>')
    x = CELL + GAP
    for t, key, bold in parts:
        o.append(f'<text x="{x:.1f}" y="{H/2+4.3:.1f}" font-family="{MONO}" font-size="{FS}" '
                 f'{"font-weight=\'700\' " if bold else ""}fill="{p[key]}">{t}</text>')
        x += (len(t)+1) * CW
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {H}" '
            f'width="{w:.1f}" height="{H}" role="img" '
            f'aria-label="{" ".join(t for t, _, _ in parts)}">{"".join(o)}</svg>\n')


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    n = views()
    specs = [
        ("linkedin", f'<path d="{ICONS["linkedin"]}"/>', "#0A66C2",
         [("Ekin Doğucan Akkaya", "ink", False)]),
        ("mail", f'<path d="{ICONS["maildotru"]}"/>', "#8B5CF6",
         [("ekinakkaya0@hotmail.com", "ink", False)]),
        ("views", EYE, "#3FB950",
         [("görüntülenme", "faint", False), (n or "—", "ink", True)]),
    ]
    for slug, icon, col, parts in specs:
        for p in (LIGHT, DARK):
            (ROOT / "assets" / f"badge-{slug}-{p['name']}.svg").write_text(
                chip(p, icon, col, parts), encoding="utf-8")
    print(f"3 rozet x 2 tema yazıldı (görüntülenme: {n or 'okunamadı'})")


if __name__ == "__main__":
    main()
