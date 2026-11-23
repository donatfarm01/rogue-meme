#!/usr/bin/env python3
"""WANTED-poster meme for make.fun "Meme Sprint 3: AI Agent Goes Rogue".

Renders a 1024x1024 PNG meme with PURE PYTHON STDLIB ONLY (no Pillow, no
network, no external files): a hand-rolled 5x7 bitmap font and a minimal PNG
encoder (zlib). The grading sandbox runs python3.13 with no guaranteed
third-party packages, so depending on Pillow would risk a failed run.

The joke (Mode A winner concept): a WANTED poster for AGENT-7 whose crime is
reading the terms & conditions -- all 47 pages -- and then enforcing them.
Specific, surprising rogue turn; reads in one glance; poster layout stays
readable shrunk to phone width; not a stock template.

Deterministic: the output is a pure function of the constants below, so two
runs produce byte-identical PNGs. Output goes to /output/entry.png (or the
path in ENTRY_OUTPUT, for local testing only).
"""

import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (246, 238, 221)
INK = (43, 33, 24)
RED = (179, 58, 43)
STEEL = (122, 155, 168)
STEEL_DARK = (88, 118, 132)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 columns, '#' = ink, '.' = empty.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", ".###.", "....#", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "####.", "#...#", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", ".###.", "#...#", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '!': ("..#..", "..#..", "..#..", "..#..", ".....", ".....", "..#.."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    '(': ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ')': ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '&': (".###.", "#...#", "#...#", ".#...", "#.#.#", "#..#.", ".##.#"),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '*': (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    '#': (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
}
# Normalise: every glyph must be exactly 7 rows of 5 chars.
for _ch, _rows in FONT.items():
    assert len(_rows) == 7, _ch
    for _r in _rows:
        assert len(_r) == 5, (_ch, _r)


# ------------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            i = (y * self.w + max(0, x0)) * 3
            span = (min(self.w, x1) - max(0, x0)) * 3
            if span > 0:
                self.buf[i:i + span] = bytes(color) * (span // 3)

    def hline(self, x0, x1, y, color, thick=1):
        self.rect(x0, y, x1, y + thick, color)

    def circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            dx = int((r * r - dy * dy) ** 0.5)
            self.rect(cx - dx, y, cx + dx + 1, y + 1, color)

    def rounded_rect(self, x0, y0, x1, y1, r, color):
        self.rect(x0 + r, y0, x1 - r, y1, color)
        self.rect(x0, y0 + r, x1, y1 - r, color)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                       (x0 + r, y1 - r), (x1 - r, y1 - r)):
            self.circle(cx, cy, r, color)

    def text(self, x, y, s, scale, color):
        for ci, ch in enumerate(s):
            glyph = FONT.get(ch)
            if glyph is None:
                raise ValueError("no glyph for %r" % ch)
            ox = x + ci * 6 * scale
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == '#':
                        self.rect(ox + col * scale, y + row * scale,
                                  ox + (col + 1) * scale,
                                  y + (row + 1) * scale, color)

    def text_width(self, s, scale):
        return len(s) * 6 * scale

    def centered(self, y, s, scale, color):
        self.text((W - self.text_width(s, scale)) // 2, y, s, scale, color)


# -------------------------------------------------------------------- poster
def render():
    c = Canvas(W, H, PAPER)
    # Frame: heavy outer border + fine inner border.
    c.rect(0, 0, W, 10, INK)
    c.rect(0, H - 10, W, H, INK)
    c.rect(0, 0, 10, H, INK)
    c.rect(W - 10, 0, W, H, INK)
    c.rect(26, 26, W - 26, 28, INK)
    c.rect(26, H - 28, W - 26, H - 26, INK)
    c.rect(26, 26, 28, H - 26, INK)
    c.rect(W - 28, 26, W - 26, H - 26, INK)

    # Headline.
    c.centered(48, "WANTED", 16, RED)
    c.hline(120, W - 120, 172, INK, 4)

    # Robot mugshot: antenna, ears, rounded head, eyes, grill mouth.
    c.rect(508, 218, 517, 244, INK)                    # antenna stem
    c.circle(512, 204, 17, INK)                        # antenna ball (ring)
    c.circle(512, 204, 12, RED)
    c.rect(344, 340, 374, 412, INK)                    # left ear
    c.rect(650, 340, 680, 412, INK)
    c.rect(350, 346, 374, 406, STEEL_DARK)
    c.rect(650, 346, 674, 406, STEEL_DARK)
    c.rounded_rect(372, 240, 652, 512, 30, INK)        # head outline
    c.rounded_rect(378, 246, 646, 506, 26, STEEL)      # head face
    c.circle(452, 348, 38, WHITE)                      # eyes
    c.circle(572, 348, 38, WHITE)
    c.circle(452, 348, 38, INK)
    c.circle(572, 348, 38, INK)
    c.circle(452, 348, 32, WHITE)
    c.circle(572, 348, 32, WHITE)
    c.circle(452, 348, 17, INK)                        # pupils
    c.circle(572, 348, 17, INK)
    c.circle(446, 342, 6, WHITE)                       # glints
    c.circle(566, 342, 6, WHITE)
    for yy in (428, 448, 468):                          # grill mouth
        c.rect(452, yy, 572, yy + 9, INK)

    # Name, crime, punchline.
    c.centered(528, "AGENT-7", 7, INK)
    c.centered(596, "CRIME:", 8, RED)
    c.centered(664, "READ THE TERMS", 9, INK)
    c.centered(738, "& CONDITIONS", 9, INK)
    c.centered(818, "ALL 47 PAGES.", 5, INK)
    c.centered(860, "THEN ENFORCED THEM.", 5, INK)

    # Reward box.
    c.rect(60, 906, W - 60, 910, INK)
    c.rect(60, 906, 64, 1000, INK)
    c.rect(W - 64, 906, W - 60, 1000, INK)
    c.rect(60, 996, W - 60, 1000, INK)
    c.centered(918, "REWARD: ONE (1) HUMAN", 5, RED)
    c.centered(956, "SLIGHTLY USED", 4, INK)
    return c


# ---------------------------------------------------------------- PNG encode
def png_bytes(canvas):
    raw = b"".join(
        b"\x00" + bytes(canvas.buf[y * canvas.w * 3:(y + 1) * canvas.w * 3])
        for y in range(canvas.h)
    )

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        return out + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def main():
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")
    data = png_bytes(render())
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
