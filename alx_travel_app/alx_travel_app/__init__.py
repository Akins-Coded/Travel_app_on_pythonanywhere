import os

USE_CELERY = os.getenv("USE_CELERY", "False").lower() == "true"

if USE_CELERY:
    try:
        from .celery import app as celery_app
        __all__ = ("celery_app",)
    except ImportError:
        celery_app = None
