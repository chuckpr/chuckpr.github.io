#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pelican.plugins import pelican_jupyter_reader

AUTHOR = 'Chuck Pepe-Ranney'
SITENAME = 'A microbiologist with a data science problem'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/chuck_pr'),
          ('github', 'https://github.com/chuckpr'),
          ('linkedin', 'https://www.linkedin.com/in/chuckpr/'))

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

TWITTER_USERNAME = 'chuckpr'
TWITTER_CARD_IMAGE_URL = 'https://www.biorxiv.org/content/biorxiv/early/2019/09/08/758359/F4.large.jpg'

PLUGINS = [pelican_jupyter_reader,]
IGNORE_FILES = ['.ipynb_checkpoints*']
SUMMARY_MAX_LENGTH = 5
