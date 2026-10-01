"""Irish Y-beam example: geometry, properties vs published, strand map.

Requires: bridgebeams (this repo), sectionproperties, matplotlib.
"""

import matplotlib.pyplot as plt

from bridgebeams.ukie import IeYBeamSection, strand_locations


def main() -> None:
    beam = IeYBeamSection("Y4")
    geom = beam.geometry
    geom.create_mesh(mesh_sizes=[5000])

    print(f"{beam.size}: depth {beam.depth:.0f} mm, Wf {beam.dimensions.top_width:.1f} mm")
    print(f"published: A = {beam.published['area']} mm^2, "
          f"yc = {beam.published['yc']} mm, Ixx = {beam.published['ixx_e9']}e9 mm^4")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 7))

    geom.plot_geometry(ax=ax1, labels=[])
    ax1.set_title(f"Irish {beam.size} beam (reconstructed profile)")

    poly = beam.polygon
    ax2.plot(*poly.exterior.xy, color="0.2")
    pts = strand_locations(beam.size)
    ax2.scatter([p[0] for p in pts], [p[1] for p in pts], s=18, marker="+", color="crimson")
    ax2.set_aspect("equal")
    ax2.set_title(f"{beam.size} - all possible strand locations")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("ie_y4_example.png", dpi=150)
    print("saved ie_y4_example.png")


if __name__ == "__main__":
    main()
