"""Build Sphinx and optionally attach the private drawing-review materials."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def replace_generated_output(candidate, output):
    """Replace generated HTML only after a successful fresh build.

    Sphinx excludes source backups, but incremental copying cannot remove old
    backups or private attachments already present in an output directory.
    """
    if output.is_symlink():
        raise ValueError(f"Refusing to replace symlink output: {output}")
    if output.exists():
        shutil.rmtree(output)
    candidate.rename(output)


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
    if output.is_symlink():
        parser.error(f"Refusing to replace symlink output: {output}")
    coverage = root / "tools/build_coverage.py"
    if coverage.is_file():
        subprocess.run([sys.executable, str(coverage)], cwd=root, check=True)
    tags = ["-t", "local_review"] if args.with_review else []
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sphinx-fresh-", dir=output.parent) as directory:
        candidate = Path(directory) / "html"
        subprocess.run(
            [sys.executable, "-m", "sphinx", "-E", "-W", *tags, "-b", "html",
             str(root / "docs/source"), str(candidate)], cwd=root, check=True,
        )
        if args.with_review:
            shutil.copy2(review, candidate / review.name)
            (candidate / "sources").symlink_to(sources, target_is_directory=True)
        replace_generated_output(candidate, output)
    if args.with_review:
        print(f"Private drawing review: {output / review.name}")
    print(f"Documentation: {output / 'index.html'}")


if __name__ == "__main__":
    main()
