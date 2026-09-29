#!/usr/bin/env python3
"""
make_test_chart.py -- draw a synthetic test image that is hard for JPEG:
saturated color bars, colored text on colored background, thin lines,
a smooth color gradient and a fine checkerboard.

  python make_test_chart.py test-chart.png
"""

import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 512, 384


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "test-chart.png"
    image = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Color bars (top), like a TV test pattern.
    bars = [(255, 255, 255), (255, 255, 0), (0, 255, 255), (0, 255, 0),
            (255, 0, 255), (255, 0, 0), (0, 0, 255), (0, 0, 0)]
    bar_width = WIDTH // len(bars)
    for i, color in enumerate(bars):
        draw.rectangle([i * bar_width, 0, (i + 1) * bar_width - 1, 95], fill=color)

    # Smooth hue gradient (middle): smooth areas compress well.
    x = np.linspace(0, 1, WIDTH)
    gradient = np.stack([
        127.5 + 127.5 * np.cos(2 * np.pi * x),
        127.5 + 127.5 * np.cos(2 * np.pi * (x - 1 / 3)),
        127.5 + 127.5 * np.cos(2 * np.pi * (x - 2 / 3)),
    ], axis=-1)
    image.paste(Image.fromarray(np.tile(gradient, (64, 1, 1)).astype(np.uint8)), (0, 96))

    # Colored text on colored backgrounds (bottom left): sharp chroma edges.
    font = ImageFont.load_default(size=40)
    draw.rectangle([0, 160, 255, 271], fill=(0, 0, 200))
    draw.text((12, 170), "JPEG", fill=(255, 40, 40), font=font)
    draw.rectangle([0, 272, 255, 383], fill=(40, 160, 40))
    draw.text((12, 282), "8 x 8", fill=(220, 0, 220), font=font)

    # Thin lines and a fine checkerboard (bottom right): high frequencies.
    for i in range(0, 128, 8):
        draw.line([(256 + i, 160), (256 + i, 271)], fill=(0, 0, 0), width=1)
        draw.line([(384, 160 + i * 112 // 128), (511, 160 + i * 112 // 128)], fill=(200, 0, 0), width=1)
    yy, xx = np.mgrid[0:112, 0:256]
    checker = ((yy // 2 + xx // 2) % 2 * 255).astype(np.uint8)
    image.paste(Image.fromarray(checker).convert("RGB"), (256, 272))

    image.save(path)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
