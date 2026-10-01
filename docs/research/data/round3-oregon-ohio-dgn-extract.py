"""Reproduce the Ohio PSID-1-13 I-beam outlines from the MicroStation V8 DGN.

Round-3 extraction helper (docs/research/round3-oregon-ohio-2026-09.md).
Needs olefile + shapely. Usage:
    python round3-oregon-ohio-dgn-extract.py sources/expansion/round2/manual/us/oh/PSID-1-13_2018-07-20.dgn
Prints each section's right-half vertices in inches (1250 UOR = 1 in).
"""
import collections, re, struct, sys, zlib

import olefile
from shapely.geometry import LineString
from shapely.geometry.polygon import orient
from shapely.ops import polygonize, unary_union


def streams(path):
    o = olefile.OleFileIO(path)
    out = {}
    for e in o.listdir(streams=True, storages=False):
        n = "/".join(e)
        b = o.openstream(n).read()
        raw = b
        for off in range(0, min(64, len(b) - 1)):
            if b[off] == 0x78 and b[off + 1] in (0x01, 0x5E, 0x9C, 0xDA):
                try:
                    raw = zlib.decompressobj().decompress(b[off:])
                    break
                except zlib.error:
                    pass
        out[n] = raw
    return out


def elements(s):
    """(type, record bytes); record length = 4 + 2 * words-to-follow (u32 at +8)."""
    for n, b in s.items():
        if "/Dgn^G/" not in n:
            continue
        p = 0
        while p + 16 <= len(b):
            typ = struct.unpack_from("<H", b, p + 4)[0]
            ln = 4 + 2 * struct.unpack_from("<I", b, p + 8)[0]
            if ln < 16 or p + ln > len(b):
                break
            yield typ, b[p:p + ln]
            p += ln


def outline_lines(s):
    """Concrete outline lines: weight 2 (sheet 1) or level 7 (WF sheets)."""
    for t, b in elements(s):
        lev = struct.unpack_from("<I", b, 0x10)[0]
        if not (b[0x34:0x38] == b"\x02\x00\x00\x00" or lev == 7):
            continue
        if t == 3:
            x1, y1, x2, y2 = struct.unpack_from("<4d", b, 0x6C)
            yield [(x1, y1), (x2, y2)]
        elif t == 4:
            k = struct.unpack_from("<I", b, 0x6C)[0]
            yield [struct.unpack_from("<2d", b, 0x74 + 16 * i) for i in range(k)]


BOXES = {  # UOR search windows (x0, x1, y0, y1)
    "II": (12035000, 12090000, 13315000, 13380000),
    "III": (12095000, 12175000, 13315000, 13390000),
    "IV": (12175000, 12265000, 13315000, 13395000),
    "MOD-IV-60": (12030000, 12115000, 13180000, 13290000),
    "MOD-IV-66": (12120000, 12205000, 13180000, 13290000),
    "MOD-IV-72": (12210000, 12300000, 13180000, 13300000),
    "WF36-49": (12055000, 12130000, 13020000, 13110000),
    "WF42-49": (12170000, 12250000, 13020000, 13115000),
    "WF48-49": (12055000, 12130000, 12890000, 12990000),
    "WF54-49": (12170000, 12250000, 12890000, 12995000),
    "WF60-49": (12285000, 12360000, 12890000, 13005000),
    "WF66-49": (12055000, 12130000, 12685000, 12800000),
    "WF72-49": (12170000, 12250000, 12685000, 12810000),
}
UOR_PER_IN = 1250.0

if __name__ == "__main__":
    lines = list(outline_lines(streams(sys.argv[1])))
    for name, (x0, x1, y0, y1) in BOXES.items():
        ls = [LineString(pl) for pl in lines
              if min(p[0] for p in pl) >= x0 and max(p[0] for p in pl) <= x1
              and min(p[1] for p in pl) >= y0 and max(p[1] for p in pl) <= y1]
        u = unary_union(list(polygonize(unary_union(ls))))
        g = orient(max(getattr(u, "geoms", [u]), key=lambda q: q.area).simplify(0.5), 1.0)
        bx0, by0, bx1, _ = g.bounds
        xc = (bx0 + bx1) / 2
        pts = {(round((x - xc) / UOR_PER_IN * 16) / 16, round((y - by0) / UOR_PER_IN * 16) / 16)
               for x, y in g.exterior.coords}
        print(name, sorted((p for p in pts if p[0] > 0), key=lambda p: (p[1], -p[0])))
