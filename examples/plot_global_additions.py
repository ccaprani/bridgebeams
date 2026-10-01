"""Render representative new/corrected sections at a common scale."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch

from bridgebeams import (
    NzIBeamSection,
    NzSuperTSection,
    QaQBeamSection,
    SepsaIGirderSection,
    TaiwanISection,
)


def main():
    output = Path(__file__).resolve().parents[1] / "docs/source/_static/images"
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams["svg.fonttype"] = "none"
    examples = [
        ("New Zealand · Super-T 1025", "RR364 S1.01 · gross approximation",
         NzSuperTSection(1025), "#c6d9e6"),
        ("New Zealand · Super-T 1225", "RR364 S1.21 · 1990 flange · gross approximation",
         NzSuperTSection(1225, top_width=1990), "#c6d9e6"),
        ("New Zealand · I-beam 1600", "RR364 S4.10 · chamfer option",
         NzIBeamSection(1600), "#c6d9e6"),
        ("Qatar · Q-girder T5", "Ashghal SD 5-1-101 · reconstruction",
         QaQBeamSection("T5"), "#e6d1b2"),
        ("Mexico · SEPSA IV-MODIFIED", "Producer profile · published-area validation",
         SepsaIGirderSection("IV-MODIFIED"), "#bddbcd"),
        ("Taiwan · Type VIII", "Freeway Bureau Fig.10 · gross midspan",
         TaiwanISection("VIII"), "#d6cde8"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(12, 8.4), layout="constrained")
    for ax, (title, subtitle, beam, color) in zip(axes.flat, examples):
        poly = beam.polygon
        ax.add_patch(PolygonPatch(poly.exterior.coords, facecolor=color,
                                  edgecolor="#243647", linewidth=1.4))
        ax.axhline(poly.centroid.y, color="#667788", linestyle="--", linewidth=0.7)
        ax.set(xlim=(-1400, 1400), ylim=(-80, 2240), aspect="equal")
        ax.set_xticks([-1000, 0, 1000])
        ax.set_yticks([0, 500, 1000, 1500, 2000])
        ax.tick_params(labelsize=8)
        ax.set_title(title + "\n" + subtitle, fontsize=9.5, pad=12)
        ax.set_xlabel("x (mm)", fontsize=8)
        ax.set_ylabel("y above soffit (mm)", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("New and corrected bridge beam profiles", fontsize=16)
    fig.supxlabel("Common scale · dashed lines show centroid height · precast gross sections, without deck or reinforcement",
                  fontsize=9)
    svg = output / "global-additions.svg"
    fig.savefig(svg)
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    fig.savefig("/tmp/bridgebeams-global-additions.png", dpi=150)
    plt.close(fig)
    print(svg)


if __name__ == "__main__":
    main()
