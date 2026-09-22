# Configuration file for the Sphinx documentation builder.
#
# For a full list of options see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

src_dir = os.path.abspath("../../src/")
sys.path.insert(0, src_dir)

from bridgebeams import __version__ as ver  # noqa: E402

# -- Project information -----------------------------------------------------

project = "bridgebeams"
copyright = "2025, Colin Caprani"
author = "Colin Caprani"

version = ver
release = ver

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "nbsphinx",
]

# Tutorials are committed with executed outputs; render rather than run.
nbsphinx_execute = "never"

myst_heading_anchors = 3
autodoc_member_order = "bysource"
autosummary_generate = True
autoclass_content = "both"
html_show_sourcelink = False
add_module_names = False

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
exclude_patterns = ["backups/**", "gen/bridgebeams.ukie*"]

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/ccaprani/bridgebeams",
}
