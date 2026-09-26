"""Build Sphinx and optionally attach the private drawing-review materials."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-review", action="store_true",
                        help="Attach ignored local HTML and source drawings; local use only")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "docs/_build/html"
    review = root / "dims_review.html"
    sources = root / "sources"
    if args.with_review and (not review.is_file() or not sources.is_dir()):
        parser.error("--with-review requires local dims_review.html and sources/")
    target = output / "sources"
    if target.exists() and not target.is_symlink():
        parser.error(f"Refusing to replace existing directory: {target}")
    coverage = root / "tools/build_coverage.py"
    if coverage.is_file():
        subprocess.run([sys.executable, str(coverage)], cwd=root, check=True)
    tags = ["-t", "local_review"] if args.with_review else []
    subprocess.run(
        [sys.executable, "-m", "sphinx", "-E", "-W", *tags, "-b", "html",
         str(root / "docs/source"), str(output)], cwd=root, check=True,
    )
    if args.with_review:
        shutil.copy2(review, output / review.name)
        if target.is_symlink():
            target.unlink()
        target.symlink_to(sources, target_is_directory=True)
        print(f"Private drawing review: {output / review.name}")
    else:
        # Prevent a later ordinary build from retaining private attachments.
        (output / review.name).unlink(missing_ok=True)
        if target.is_symlink():
            target.unlink()
    print(f"Documentation: {output / 'index.html'}")


if __name__ == "__main__":
    main()
