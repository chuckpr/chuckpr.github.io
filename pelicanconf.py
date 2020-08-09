#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = "Chuck Pepe-Ranney"
SITENAME = "A microbiologist with a data science problem"
SITEURL = ""
DESCRIPTION = """A microbiology-themed technical blog for data scientists."""

PATH = "content"

TIMEZONE = "US/Eastern"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "http://getpelican.com/"),
    ("Python.org", "http://python.org/"),
    ("Jinja2", "http://jinja.pocoo.org/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("twitter", "https://twitter.com/chuck_pr"),
    ("github", "https://github.com/chuckpr"),
    ("linkedin", "https://www.linkedin.com/in/chuckpr/"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

TWITTER_USERNAME = "chuckpr"
TWITTER_IMAGE_URL = "https://res.cloudinary.com/chuckpr-github-io/image/upload/v1596935417/twitter_card_image_r4xodj.png"

IGNORE_FILES = [".ipynb_checkpoints*"]
SUMMARY_MAX_LENGTH = 15
STATIC_PATHS = ["images", "notebooks/images", "extra"]
EXTRA_PATH_METADATA = {"images/favicon.ico": {"path": "favicon.ico"}}

if os.environ.get("PELICAN_THEME", None) is not None:
    THEME = os.environ["PELICAN_THEME"]

from pelican.plugins import pelican_jupyter_reader

PLUGINS = [
    pelican_jupyter_reader,
]

# # Uncomment for plugin development
# if os.environ.get('PELICAN_PLUGIN_PATHS', None) is not None:
#     PLUGIN_PATHS = os.environ['PELICAN_PLUGIN_PATHS'].split(':')
#     PLUGINS = ['pelican_jupyter_reader',]

import extended_sitemap

PLUGINS.append(extended_sitemap)

TOGGLE_ALL_TAG = "toggle_all"
TOGGLE_CODE_TAG = "toggle_code"
TOGGLE_CODE_BUTTON_TEXT = "toggle code"
TOGGLE_ALL_BUTTON_TEXT = "show me"
HIDE_CELL_TAG = "disappear"


# Theme settings
NAV_LINKS = [
    ("about", "pages/about/"),
]
EXTRA_CSS = dict(article="extra/css/notebook.css")
CLOUDINARY_URL = (
    "https://res.cloudinary.com/chuckpr-github-io/"
    "image/upload/co_rgb:f2f2f2,w_1200,c_fit,g_east,"
    "x_100,l_text:Helvetica_110_right:"
)
CLOUDINARY_IMAGE = "blog_card.png"
CLOUDINARY_INDEX_IMAGE = "blog_index_card.png"

# Instantiate a config object and call it NBCONVERT_CONFIG
from traitlets.config import Config

NBCONVERT_CONFIG = Config()

# This removes Jupyter input prompts
NBCONVERT_CONFIG.HTMLExporter.exclude_input_prompt = True

# This makes Jupyter magic cells have proper code highlighting
# regardless of the language of the notebook kernel
NBCONVERT_CONFIG.HighlightMagicsPreprocessor.enabled = True
NBCONVERT_CONFIG.HighlightMagicsPreprocessor.languages.update(
    {"%%svg": "xml", "%%html": "html"}
)

# select the nbconvert template
NBCONVERT_CONFIG.HTMLExporter.template_path.append(".")
NBCONVERT_CONFIG.HTMLExporter.template_file = "blog"

# extract images to files
NBCONVERT_CONFIG.ExtractOutputPreprocessor.enabled = True
NBCONVERT_CONFIG.ExtractOutputPreprocessor.output_filename_template = (
    "images/{unique_key}_{cell_index}_{index}{extension}"
)

# adujst the anchor links
NBCONVERT_CONFIG.HTMLExporter.anchor_link_text = " ⇦"
