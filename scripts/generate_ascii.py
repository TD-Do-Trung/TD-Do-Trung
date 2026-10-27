#!/usr/bin/env python3
"""Generate a self-contained animated ASCII portrait SVG for GitHub profile READMEs.
Requires: Pillow. All animation uses SMIL, without JavaScript or external assets.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageEnhance, ImageOps


def generate(image_path: Path, out_path: Path, name: str, handle: str, columns: int, duration: float) -> None:
    # Monospace glyphs are taller than they are wide; sample a near-square portrait.
    rows = round(columns * 0.63)
    cell_w = 7.15
    cell_h = 11.5
    art_w = columns * cell_w
    art_h = rows * cell_h
    pad_x, art_top = 34.0, 65.0
    width = art_w + 2 * pad_x
    height = art_top + art_h + 66
    palette = "@%#*+=-:. "  # dark pixels -> dense characters, white -> space

    with Image.open(image_path) as src:
        src = src.convert("RGBA")
        # Transparent portrait backgrounds become white so they map to spaces.
        background = Image.new("RGBA", src.size, "white")
        background.alpha_composite(src)
        grayscale = ImageOps.grayscale(background.convert("RGB"))
        grayscale = ImageOps.autocontrast(grayscale, cutoff=1)
        grayscale = ImageEnhance.Contrast(grayscale).enhance(1.25)
        samples = ImageOps.fit(
            grayscale, (columns, rows), method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.42),
        )

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" role="img" aria-label="Animated ASCII portrait of {escape(name)}">',
        '<rect width="100%" height="100%" rx="14" fill="#0d1117"/>',
        f'<rect x=".5" y=".5" width="{width-1:.1f}" height="{height-1:.1f}" rx="14" fill="none" stroke="#30363d"/>',
        f'<path d="M 0 40 H {width:.1f}" stroke="#30363d"/>',
    ]
    for idx, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        pieces.append(f'<circle cx="{18 + 17 * idx}" cy="20" r="5" fill="{color}"/>')
    pieces.append(
        f'<text x="{width/2:.1f}" y="24" fill="#8b949e" font-size="13" '
        f'font-family="monospace" text-anchor="middle">{escape(handle)}@github:~$ ./portrait.sh</text>'
    )
    pixels = samples.load()
    row_time = duration / rows
    for row_index in range(rows):
        line = "".join(palette[round(pixels[col, row_index] / 255 * (len(palette) - 1))] for col in range(columns))
        top = art_top + row_index * cell_h
        baseline = top + cell_h * 0.83
        start = row_index * row_time
        animation_time = row_time * 1.8
        # Animated clipping windows reveal every row from left to right.
        pieces.append(
            f'<defs><clipPath id="line-{row_index}"><rect x="{pad_x:.1f}" y="{top:.1f}" '
            f'width="0" height="{cell_h+1:.1f}"><animate attributeName="width" from="0" '
            f'to="{art_w:.1f}" begin="{start:.3f}s" dur="{animation_time:.3f}s" '
            'fill="freeze"/></rect></clipPath></defs>'
        )
        pieces.append(
            f'<text x="{pad_x:.1f}" y="{baseline:.1f}" font-family="monospace" '
            f'font-size="11.6" fill="#c9d1d9" xml:space="preserve" '
            f'textLength="{art_w:.1f}" lengthAdjust="spacing" '
            f'clip-path="url(#line-{row_index})">{escape(line)}</text>'
        )
    bottom = art_top + art_h + 18
    pieces.append(
        f'<path d="M 0 {bottom:.1f} H {width:.1f}" stroke="#30363d"/>'
        f'<text x="{pad_x:.1f}" y="{bottom+28:.1f}" fill="#8b949e" '
        f'font-size="14" font-family="monospace">{escape(handle)}@github:~$ whoami '
        f'<tspan fill="#c9d1d9">{escape(name)}</tspan></text>'
        '</svg>'
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(pieces), encoding="utf-8")
    print(f"Generated {out_path} ({width:.0f} x {height:.0f})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to a clear headshot (preferably white/transparent background)")
    parser.add_argument("--out", type=Path, default=Path("assets/neildo-ascii.svg"))
    parser.add_argument("--name", default="Neil Do")
    parser.add_argument("--handle", default="neildo")
    parser.add_argument("--columns", type=int, default=100)
    parser.add_argument("--duration", type=float, default=5.5, help="Reveal duration in seconds")
    args = parser.parse_args()
    if not 30 <= args.columns <= 200:
        parser.error("--columns must be between 30 and 200")
    if args.duration <= 0:
        parser.error("--duration must be greater than zero")
    generate(args.image, args.out, args.name, args.handle, args.columns, args.duration)
