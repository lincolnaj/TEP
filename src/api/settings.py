import ast
import os
import re


def env(key, default=None, valuetype=str, required=False, nullable=bool):
    if required and (key not in os.environ):
        raise RuntimeError(f"Required environment settings {key} not found")
    if valuetype == bool:
        raw_val = default
        if key in os.environ:
            raw_val = ast.literal_eval(os.environ.get(key))
    elif valuetype == list:
        raw_val = default
        if key in os.environ:
            raw_val = re.split(r", ?", os.environ.get(key))
    else:
        raw_val = os.environ.get(key, default)
    val = valuetype(raw_val)
    if nullable and (default is None) and (raw_val == default):
        val = default
    return val


DEBUG = not env("PRODUCTION_MODE", valuetype=bool, default=False)

if DEBUG:
    DEV_HOST = env("FLASK_DEV_HOST", valuetype=str, default="127.0.0.1")
    DEV_PORT = env("FLASK_DEV_PORT", valuetype=int, default=5000)

API_HISTORICAL_DAYS_LOOKBACK = env(
    "API_HISTORICAL_DAYS_LOOKBACK", valuetype=int, default=61
)

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", valuetype=str, required=True)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", valuetype=str, required=True)
AWS_REGION_NAME = env("AWS_REGION_NAME", valuetype=str, required=True)

AWS_ATHENA_SCHEMA = env("AWS_ATHENA_SCHEMA", valuetype=str, default="default")
AWS_ATHENA_DATABASE_NAME = env("AWS_ATHENA_DATABASE_NAME", valuetype=str, required=True)
AWS_ATHENA_MAX_WORKERS = env("AWS_ATHENA_MAX_WORKERS", valuetype=int, default=1)
AWS_ATHENA_POLL_INTERVAL = env("AWS_ATHENA_POLL_INTERVAL", valuetype=int, default=1)
AWS_ATHENA_S3_RESULT_DIR = env("AWS_ATHENA_S3_RESULT_DIR", valuetype=str, required=True)

AWS_REDSHIFT_HOST = env("AWS_REDSHIFT_HOST", valuetype=str, required=True)
AWS_REDSHIFT_PORT = env("AWS_REDSHIFT_PORT", valuetype=int, default=5439)
AWS_REDSHIFT_USER = env("AWS_REDSHIFT_USER", valuetype=str, required=True)
AWS_REDSHIFT_PASS = env("AWS_REDSHIFT_PASS", valuetype=str, required=True)
AWS_REDSHIFT_SCHEMA = env("AWS_REDSHIFT_SCHEMA", valuetype=str, default="default")
AWS_REDSHIFT_DATABASE_NAME = env(
    "AWS_REDSHIFT_DATABASE_NAME", valuetype=str, required=True
)
AWS_REDSHIFT_MIN_CONNECTIONS = env(
    "AWS_REDSHIFT_MIN_CONNECTIONS", valuetype=int, default=1
)
AWS_REDSHIFT_MAX_CONNECTIONS = env(
    "AWS_REDSHIFT_MAX_CONNECTIONS", valuetype=int, default=1
)

MW_SPATIAL_API_HOST = env("MW_SPATIAL_API_HOST", valuetype=str, required=True)
MW_SPATIAL_API_PORT = env("MW_SPATIAL_API_PORT", valuetype=int, default=80)
MW_SPATIAL_API_ADMINISTRATIVE_DIVISION_ENDPOINT = env(
    "MW_SPATIAL_API_ADMINISTRATIVE_DIVISION_ENDPOINT", valuetype=str, required=True
)

REDIS_HOST = env("REDIS_HOST", valuetype=str, required=True)
REDIS_PORT = env("REDIS_PORT", valuetype=int, default=6379)
REDIS_PASS = env("REDIS_PASSWORD", valuetype=str, required=True)
REDIS_DATABASE_INDEX = env("REDIS_DATABASE_INDEX", valuetype=int, required=True)

MONGODB_URI = env('MONGODB_URI', valuetype=str, required=True)
MONGODB_MASTER_DB_NAME = env('MONGODB_MASTER_DB_NAME', valuetype=str, required=True)

LOGGER_HOST = env("LOGGER_HOST", valuetype=str, required=True)
LOGGER_PORT = env("LOGGER_PORT", valuetype=int, default=24224)
