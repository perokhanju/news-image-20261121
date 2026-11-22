#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os, math

def build():
    img = Image.open("art_raw.png").convert("RGBA")
    w, h = img.size
    img = img.crop((0, 0, w, h - 60))
    tw, th = 1024, 1024
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    cx, cy = nw // 2, nh // 2
    img = img.crop((cx - tw // 2, cy - th // 2, cx - tw // 2 + tw, cy - th // 2 + th))

    overlay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(min(400, th)):
        alpha = int(200 * (1 - y / 400))
        od.line([(0, y), (tw - 1, y)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    serif_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font_mast = ImageFont.truetype(serif_bold, 84)
    font_date = ImageFont.truetype(sans, 32)
    font_head1 = ImageFont.truetype(serif_bold, 54)
    font_head2 = ImageFont.truetype(sans, 30)

    mast_text = "THE WORLD"
    bw = draw.textbbox((0, 0), mast_text, font=font_mast)[2]
    draw.text(((tw - bw) // 2, 30), mast_text, font=font_mast, fill=(245, 241, 232))

    date_text = "SATURDAY, NOVEMBER 21, 2026"
    bw = draw.textbbox((0, 0), date_text, font=font_date)[2]
    draw.text(((tw - bw) // 2, 122), date_text, font=font_date, fill=(255, 184, 77))

    pad = 20
    band = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)

    h1_text = "KILLER ROBOT TALKS FAIL"
    bbox = draw.textbbox((0, 0), h1_text, font=font_head1)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x1, y1 = (tw - bw) // 2, 220
    region = img.crop((x1, y1, x1 + bw, y1 + bh)).convert("L")
    if region.getextrema()[1] > 150:
        bd.rounded_rectangle(
            [x1 - pad, y1 - pad, x1 + bw + pad, y1 + bh + pad],
            radius=14, fill=(0, 0, 0, 165),
        )

    h2_text = "UN Geneva talks end with no binding rules — 2 more years of talk"
    bbox = draw.textbbox((0, 0), h2_text, font=font_head2)
    bw2, bh2 = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x2, y2 = (tw - bw2) // 2, 310
    bd.rounded_rectangle(
        [x2 - pad, y2 - pad, x2 + bw2 + pad, y2 + bh2 + pad],
        radius=14, fill=(0, 0, 0, 170),
    )
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)

    draw.text((x1, y1), h1_text, font=font_head1, fill=(245, 241, 232))
    ux1, uy = x1, y1 + bh + 4
    draw.line([(ux1, uy), (ux1 + bw, uy)], fill=(180, 30, 30), width=2)

    draw.text((x2, y2), h2_text, font=font_head2, fill=(200, 195, 180))

    font_label = ImageFont.truetype(sans, 22)
    bottom_text = "IRAN STRIKES 3 TANKERS  \u2022  CARTEL BOSS 'EL CHAPO ISIDRO' CAUGHT  \u2022  AI STOCKS TUMBLE  \u2022  UN COURT: MYANMAR GENOCIDE"
    bbox = draw.textbbox((0, 0), bottom_text, font=font_label)
    total_w = bbox[2] - bbox[0]
    max_w = tw - 40

    if total_w <= max_w:
        lines = [bottom_text]
    else:
        parts = bottom_text.split("  \u2022  ")
        mid = len(parts) // 2
        lines = ["  \u2022  ".join(parts[:mid]), "  \u2022  ".join(parts[mid:])]

    strip_y = 935
    strip_h = 75
    draw.rectangle([(0, strip_y), (tw, strip_y + strip_h)], fill=(0, 0, 0, 200))

    line_h = 32
    start_y = strip_y + (strip_h - len(lines) * line_h) // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_label)
        bw_l = bbox[2] - bbox[0]
        draw.text(((tw - bw_l) // 2, start_y + i * line_h), line, font=font_label, fill=(220, 215, 200))

    out = img.convert("RGB")
    os.makedirs("app", exist_ok=True)
    out.save("app/entry.png", "PNG", optimize=True)
    size = os.path.getsize("app/entry.png")
    print(f"Done: app/entry.png  {out.width}x{out.height}  {size/1024:.1f} KiB")

if __name__ == "__main__":
    build()
