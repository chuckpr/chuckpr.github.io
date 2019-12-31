# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = 'pelicanconf.py'
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    'settings_base': SETTINGS_FILE_BASE,
    'settings_publish': 'publishconf.py',
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    'deploy_path': SETTINGS['OUTPUT_PATH'],
    # Port for `serve`
    'port': 8000,
}

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c, theme_path=''):
    """Build local version of site"""
    if theme_path:
        CONFIG.update({'theme_path': theme_path})
        c.run('pelican -t {theme_path} -s {settings_base}'.format(**CONFIG))
    else:
        c.run('pelican -s {settings_base}'.format(**CONFIG))

@task
def rebuild(c, theme_path=''):
    """`build` with the delete switch"""
    if theme_path:
        CONFIG.update({'theme_path': theme_path})
        c.run('pelican -d -t {theme_path} -s {settings_base}'.format(**CONFIG))
    else:
        c.run('pelican -d -s {settings_base}'.format(**CONFIG))

# @task
# def regenerate(c):
#     """Automatically regenerate site upon file modification"""
#     c.run('pelican -r -s {settings_base}'.format(**CONFIG))

@task
def serve(c):
    """Serve site at http://localhost:$PORT/ (default port is 8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s {settings_publish}'.format(**CONFIG))

@task
def livereload(c, theme_path=''):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server
    build(c, theme_path=theme_path)
    server = Server()
    # Watch the base settings file
    server.watch(CONFIG['settings_base'],
                 lambda: build(c, theme_path=theme_path))
    # Watch content source files
    content_file_extensions = ['.md', '.rst', '.ipynb']
    for extension in content_file_extensions:
        content_blob = '{0}/**/*{1}'.format(SETTINGS['PATH'], extension)
        server.watch(content_blob, lambda: build(c, theme_path=theme_path))
    # Watch the theme's templates and static assets
    if theme_path:
        server.watch('{}/templates/*.html'.format(theme_path),
                     lambda: build(c, theme_path=theme_path))
        static_file_extensions = ['.css', '.js', '.svg']
        for extension in static_file_extensions:
            static_file = '{0}/static/**/*{1}'.format(theme_path, extension)
            server.watch(static_file, lambda: build(c, theme_path=theme_path))
    # Serve output path on configured port
    server.serve(port=CONFIG['port'], root=CONFIG['deploy_path'])

@task
def publish(c, theme_path=''):
    if theme_path:
        CONFIG.update({'theme_path': theme_path})
        c.run('pelican -t {theme_path} -s {settings_publish}'.format(**CONFIG))
    else:
        c.run('pelican -s {settings_publish}'.format(**CONFIG))
