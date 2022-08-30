# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os.path
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath('../../complex'))
sys.path.extend(
    [
        # numpy standard doc extensions
        os.path.join(os.path.dirname(__file__), "..", "../..", "sphinxext")
    ]
)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'complex'
copyright = f"{datetime.now().year}, Advestis"
author = 'Advestis'
source_suffix = [".md", ".rst"]
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'numpydoc',
    'm2r2'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_theme_options = {
    "external_links": [],
    "github_url": "https://github.com/Advestis",
}
html_favicon = "../web/favicon.png"
html_logo = "../web/favicon.jpg"
