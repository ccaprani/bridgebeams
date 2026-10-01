"""Render representative profiles unlocked by the September visual review."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch

from bridgebeams import (
    CivilconYBeamSection, IeWBeamSection, NoNtbKtbSection, NzHollowCoreSection,
)


def main():
    examples = [
        ("Norway NTB1400", "15 mm bottom chamfers: reviewer interpretation",
         NoNtbKtbSection("NTB800-400x1400"), "#bddbcd"),
        ("Norway KTB1400", "Asymmetric outer face: 30 mm horizontal offset",
         NoNtbKtbSection("KTB570-400x1400"), "#bddbcd"),
        ("New Zealand 587 · inner", "Two circular voids; source shear keys",
         NzHollowCoreSection(587, "inner"), "#c6d9e6"),
        ("New Zealand 587 · outer", "One circular void; optional drip groove omitted",
         NzHollowCoreSection(587, "outer"), "#c6d9e6"),
        ("Civilcon Y8", "40 × 50 mm ledges; R100 web junction",
         CivilconYBeamSection("Y8"), "#d6cde8"),
        ("Banagher W19", "Straight internal faces; current manual dimensions",
         IeWBeamSection("W19"), "#e6d1b2"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(12, 9), layout="constrained")
    plt.rcParams["svg.fonttype"] = "none"
    for ax, (title, note, section, color) in zip(axes.flat, examples):
        polygon = section.polygon
        centre_x = (polygon.bounds[0] + polygon.bounds[2]) / 2
        vertices, codes = [], []
        for ring in [polygon.exterior, *polygon.interiors]:
            points = [(x - centre_x, y) for x, y in ring.coords]
            vertices.extend(points)
            codes.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(points)-2) + [MplPath.CLOSEPOLY])
        ax.add_patch(PathPatch(MplPath(vertices, codes), facecolor=color,
                               edgecolor="#243647", linewidth=1.2))
        ax.axhline(polygon.centroid.y, color="#667788", linestyle="--", linewidth=.7)
        ax.set(xlim=(-1200, 1200), ylim=(-80, 2400), aspect="equal")
        ax.set_title(title + "\n" + note, fontsize=9)
        ax.set_xlabel("x relative to bounding-box centre (mm)", fontsize=8)
        ax.set_ylabel("y above soffit (mm)", fontsize=8)
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Profiles added after visual review", fontsize=16)
    fig.supxlabel("Common scale · gross precast concrete · dashed lines show centroid height", fontsize=9)
    output = Path(__file__).resolve().parents[1] / "docs/source/_static/images/review-additions.svg"
    fig.savefig(output)
    output.write_text("\n".join(line.rstrip() for line in output.read_text().splitlines()) + "\n")
    fig.savefig("/tmp/bridgebeams-review-additions.png", dpi=150)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
