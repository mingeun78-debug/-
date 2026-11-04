"""NUTSHLY 넛슬리 logo generator: all text converted to vector outlines."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg

BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "npmf")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONTS = {
    "cinzel": TTFont(f"{F}/fontsource-cinzel-5.3.0/package/files/cinzel-latin-600-normal.woff2"),
    "kr": TTFont(f"{F}/fontsource-noto-serif-kr-5.3.1/package/files/noto-serif-kr-korean-600-normal.woff2"),
    "corm": TTFont(f"{F}/fontsource-cormorant-garamond-5.3.0/package/files/cormorant-garamond-latin-600-normal.woff2"),
}

BROWN, GOLD = "#4A3324", "#B08D57"


def measure(font, text, size, tracking=0.0):
    upm = font["head"].unitsPerEm
    cmap, hmtx = font.getBestCmap(), font["hmtx"]
    s = size / upm
    w = sum(hmtx[cmap[ord(c)]][0] * s for c in text)
    return w + tracking * size * (len(text) - 1)


def text_path(font, text, size, x, y, tracking=0.0, anchor="middle"):
    """Return SVG path 'd' for text, baseline at y."""
    upm = font["head"].unitsPerEm
    cmap, hmtx, gs = font.getBestCmap(), font["hmtx"], font.getGlyphSet()
    s = size / upm
    if anchor == "middle":
        x -= measure(font, text, size, tracking) / 2
    pen = SVGPathPen(gs)
    for c in text:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
        x += hmtx[g][0] * s + tracking * size
    return pen.getCommands()


def almond(cx, cy, h, color, stroke=None):
    """Simple almond / nut mark: pointed oval with a center groove."""
    # teardrop almond: pointed top, broad rounded bottom, fine skin lines
    w = h * 0.66
    t, b = cy - h / 2, cy + h / 2
    outer = (f"M{cx},{t} C{cx + w * 0.30},{t + h * 0.18} {cx + w * 0.56},{cy + h * 0.02} {cx + w * 0.50},{cy + h * 0.26} "
             f"C{cx + w * 0.44},{b - h * 0.02} {cx - w * 0.44},{b - h * 0.02} {cx - w * 0.50},{cy + h * 0.26} "
             f"C{cx - w * 0.56},{cy + h * 0.02} {cx - w * 0.30},{t + h * 0.18} {cx},{t} Z")
    sw = h * 0.028
    lines = [
        f"M{cx - w * 0.06},{t + h * 0.22} C{cx - w * 0.20},{cy} {cx - w * 0.20},{cy + h * 0.20} {cx - w * 0.10},{b - h * 0.14}",
        f"M{cx + w * 0.10},{t + h * 0.30} C{cx + w * 0.22},{cy + h * 0.04} {cx + w * 0.20},{cy + h * 0.20} {cx + w * 0.14},{b - h * 0.18}",
    ]
    skin = "".join(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw:.2f}" stroke-linecap="round"/>' for d in lines)
    return f'<path d="{outer}" fill="{color}"/>' + skin


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"{rect}{body}</svg>")


def stacked(main, accent, groove, bg=None):
    W, H = 1200, 760
    cx = W / 2
    b = [almond(cx, 120, 110, accent, groove if groove else (bg or "#fff"))]
    b.append(f'<path d="{text_path(FONTS["cinzel"], "NUTSHLY", 170, cx, 400, 0.10)}" fill="{main}"/>')
    # gold rules with 넛슬리 in the middle
    kw = measure(FONTS["kr"], "넛슬리", 84, 0.18)
    gap, ln = 40, 230
    y = 500
    for x1, x2 in ((cx - kw / 2 - gap - ln, cx - kw / 2 - gap), (cx + kw / 2 + gap, cx + kw / 2 + gap + ln)):
        b.append(f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{accent}" stroke-width="3"/>')
    b.append(f'<path d="{text_path(FONTS["kr"], "넛슬리", 84, cx, 530, 0.18)}" fill="{main}"/>')
    b.append(f'<path d="{text_path(FONTS["corm"], "HOMEMADE ROASTED NUTS", 46, cx, 660, 0.28)}" fill="{accent}"/>')
    return svg(W, H, "".join(b), bg)


def horizontal(main, accent, groove, bg=None):
    W, H = 1600, 360
    nut_h = 150
    en = measure(FONTS["cinzel"], "NUTSHLY", 150, 0.08)
    kr = measure(FONTS["kr"], "넛슬리", 96, 0.12)
    gap = 60
    total = nut_h * 0.62 + gap + en + gap + 3 + gap + kr
    x = (W - total) / 2
    b = [almond(x + nut_h * 0.31, 175, nut_h, accent, groove if groove else (bg or "#fff"))]
    x += nut_h * 0.62 + gap
    b.append(f'<path d="{text_path(FONTS["cinzel"], "NUTSHLY", 150, x, 230, 0.08, "start")}" fill="{main}"/>')
    x += en + gap
    b.append(f'<line x1="{x:.1f}" y1="105" x2="{x:.1f}" y2="245" stroke="{accent}" stroke-width="3"/>')
    x += 3 + gap
    b.append(f'<path d="{text_path(FONTS["kr"], "넛슬리", 96, x, 210, 0.12, "start")}" fill="{main}"/>')
    return svg(W, H, "".join(b), bg)


VARIANTS = {
    "NUTSHLY_logo_main_color": stacked(BROWN, GOLD, "#FFFFFF"),
    "NUTSHLY_logo_horizontal_color": horizontal(BROWN, GOLD, "#FFFFFF"),
    "NUTSHLY_logo_main_black": stacked("#000000", "#000000", "#FFFFFF"),
    "NUTSHLY_logo_main_white": stacked("#FFFFFF", "#FFFFFF", BROWN, bg=BROWN),
}

for name, s in VARIANTS.items():
    with open(f"{OUT}/{name}.svg", "w") as fh:
        fh.write(s)
    pdf = cairosvg.svg2pdf(bytestring=s.encode())
    with open(f"{OUT}/{name}.pdf", "wb") as fh:
        fh.write(pdf)
    # Illustrator (CS+) .ai files are PDF-based; Illustrator opens this as editable vector paths.
    with open(f"{OUT}/{name}.ai", "wb") as fh:
        fh.write(pdf)
    cairosvg.svg2eps(bytestring=s.encode(), write_to=f"{OUT}/{name}.eps")
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}.png", output_width=2400)
print("done", list(VARIANTS))
