#! /usr/bin/env python

import asyncio

from flask import Flask
from flask_restful import Api

from api import settings


from persistence.mongodb import MongoDbClient
from geocode.spatial import MWSpatialAPIClient


# FIXME: Consider migrating to async workers in the future
# Using flask-aiohttp library
app = Flask(__name__)
api = Api(app)
async_event_loop = asyncio.get_event_loop()

mongodb_client = MongoDbClient(settings.MONGODB_URI)
api_backend_resource = {
    "mongodb_client": mongodb_client,
}


# TimeBelted Range Frequency Moblie SDK routing
api.add_resource(
    class,
    "api",
    resource_class_kwargs=api_backend_resource,
    endpoint="",
)



# /health
api.add_resource(HealthCheckAPIView, "/health", endpoint="health_check_endpoint")


if __name__ == "__main__":
    app.run(
        host=settings.DEV_HOST,
        port=settings.DEV_PORT,
        debug=settings.DEBUG,
        use_reloader=settings.DEBUG,
        use_debugger=settings.DEBUG,
    )
