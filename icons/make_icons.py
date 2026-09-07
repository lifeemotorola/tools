#!/usr/bin/env python3
"""Write PNG app icons without Pillow / rsvg."""
from __future__ import annotations

import math
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
NAVY = (30, 58, 138, 255)
WHITE = (255, 255, 255, 255)
PAGE = (224, 231, 255, 255)
BLUE = (59, 130, 246, 255)
GOLD = (245, 158, 11, 255)
INK = (30, 58, 138, 255)


def new_img(size: int, color=NAVY):
    return [list(color) for _ in range(size * size)], size


def setp(img, size, x, y, color):
    if 0 <= x < size and 0 <= y < size:
        img[y * size + x] = list(color)


def blend(img, size, x, y, color):
    if not (0 <= x < size and 0 <= y < size):
        return
    src = img[y * size + x]
    a = color[3] / 255.0
    if a >= 1:
        img[y * size + x] = list(color)
        return
    out = [int(color[i] * a + src[i] * (1 - a)) for i in range(3)] + [255]
    img[y * size + x] = out


def fill_rect(img, size, x0, y0, x1, y1, color):
    x0, x1 = int(min(x0, x1)), int(max(x0, x1))
    y0, y1 = int(min(y0, y1)), int(max(y0, y1))
    for y in range(max(0, y0), min(size, y1)):
        row = y * size
        for x in range(max(0, x0), min(size, x1)):
            img[row + x] = list(color)


def fill_round_rect(img, size, x0, y0, x1, y1, r, color):
    x0, y0, x1, y1, r = int(x0), int(y0), int(x1), int(y1), int(r)
    for y in range(max(0, y0), min(size, y1)):
        for x in range(max(0, x0), min(size, x1)):
            dx = 0
            dy = 0
            if x < x0 + r:
                dx = x0 + r - x
            elif x >= x1 - r:
                dx = x - (x1 - r - 1)
            if y < y0 + r:
                dy = y0 + r - y
            elif y >= y1 - r:
                dy = y - (y1 - r - 1)
            if dx and dy:
                if dx * dx + dy * dy <= r * r:
                    img[y * size + x] = list(color)
            else:
                img[y * size + x] = list(color)


def fill_circle(img, size, cx, cy, r, color):
    r2 = r * r
    x0, x1 = int(cx - r - 1), int(cx + r + 2)
    y0, y1 = int(cy - r - 1), int(cy + r + 2)
    for y in range(y0, y1):
        for x in range(x0, x1):
            d = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            if d <= r2:
                setp(img, size, x, y, color)
            elif d <= (r + 0.6) ** 2:
                a = max(0, 1 - (math.sqrt(d) - r))
                blend(img, size, x, y, (color[0], color[1], color[2], int(255 * a)))


def thick_line(img, size, x0, y0, x1, y1, w, color, dashed=False):
    steps = max(int(math.hypot(x1 - x0, y1 - y0) * 2), 1)
    hw = w / 2
    for i in range(steps + 1):
        t = i / steps
        if dashed and int(t * 18) % 2:
            continue
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        fill_circle(img, size, x, y, hw, color)


def draw_card_art(img, size, pad=0.0):
    """Draw the booklet mark in a 0–64 design space, scaled to size with optional pad (0–1)."""
    s = size * (1 - 2 * pad)
    o = size * pad

    def X(v):
        return o + v / 64.0 * s

    def Y(v):
        return o + v / 64.0 * s

    def U(v):
        return v / 64.0 * s

    fill_rect(img, size, X(12), Y(16), X(30), Y(50), WHITE)
    fill_rect(img, size, X(34), Y(16), X(52), Y(50), PAGE)
    thick_line(img, size, X(31), Y(14), X(31), Y(52), max(1.2, U(1.6)), INK, dashed=True)
    for yy in (24, 30, 36, 42):
        thick_line(img, size, X(16), Y(yy), X(26), Y(yy), max(1.1, U(1.5)), INK)
        thick_line(img, size, X(38), Y(yy), X(48), Y(yy), max(1.1, U(1.5)), BLUE)
    fill_circle(img, size, X(49), Y(15), U(9), GOLD)
    thick_line(img, size, X(45), Y(15), X(48), Y(18), max(1.4, U(2.2)), WHITE)
    thick_line(img, size, X(48), Y(18), X(53), Y(12), max(1.4, U(2.2)), WHITE)


def write_png(path, img, size):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        row = y * size
        for x in range(size):
            raw.extend(img[row + x][:4])

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    blob = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(blob)
    print("wrote", path, size, "bytes", len(blob))


def make(path, size, maskable=False):
    if maskable:
        img, n = new_img(size, NAVY)
        draw_card_art(img, n, pad=0.14)
    else:
        img, n = new_img(size, (0, 0, 0, 0))
        r = size * 0.22
        fill_round_rect(img, n, 0, 0, size, size, r, NAVY)
        draw_card_art(img, n, pad=0.0)
    write_png(path, img, n)


def main():
    make(os.path.join(ROOT, "icon-192.png"), 192)
    make(os.path.join(ROOT, "icon-512.png"), 512)
    make(os.path.join(ROOT, "icon-maskable-192.png"), 192, maskable=True)
    make(os.path.join(ROOT, "icon-maskable-512.png"), 512, maskable=True)
    make(os.path.join(ROOT, "apple-touch-icon.png"), 180)


if __name__ == "__main__":
    main()
