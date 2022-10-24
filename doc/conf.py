# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py_auth_micro"
copyright = "2022, Ole Hannemann"
author = "Ole Hannemann"

import os
import sys
import re

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))


def get_version():
    versionline = open("../py_auth_micro/_version.py", "rt").read()
    mob = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionline, re.M)
    if mob:
        return mob.group(1)
    else:
        raise RuntimeError("Unable to find version string")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_immaterial",
]

# Todo settings
todo_include_todos = True
todo_emit_warnings = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = True

autodoc_default_options = {
    "member-order": "bysource",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_show_sourcelink = True

html_theme = "sphinx_immaterial"


# material theme options (see theme.conf for more information)
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
    },
    "site_url": "https://bad-microservices.github.io/py_auth_micro/",
    "repo_url": "https://github.com/bad-microservices/py_auth_micro",
    "repo_name": "py_auth_micro",
    "repo_type": "github",
    "edit_uri": "blob/main/doc",
    # "google_analytics": ["UA-XXXXX", "auto"],
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "toc.follow",
        "toc.sticky",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-green",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    # BEGIN: version_dropdown
    "version_dropdown": True,
    "version_info": [
        {
            "version": "https://bad-microservices.github.io/py_auth_micro",
            "title": "Github Pages",
            "aliases": [],
        },
    ],
    # END: version_dropdown
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/bad-microservices/py_auth_micro",
        },
        {
            "icon": "fontawesome/brands/discord",
            "link": "https://discord.gg/7HUxPP9QNS",
        },
    ],
    # END: social icons
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_immaterial"
html_static_path = ["_static"]

# The master toctree document.
master_doc = "toc"
