#! /usr/bin/env python

from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from api.data import app as application


def make_aiohttp_app(app):
    wsgi_handler = WSGIHandler(application)
    aioapp = web.Application()
    aioapp.router.add_route("*", "/{path_info:.*}", wsgi_handler)

    return aioapp


aioapp = make_aiohttp_app(application)
