from django.conf import settings


def run_task(task_func, *args, **kwargs):
    """
    Run Celery task asynchronously if USE_CELERY=True,
    else run synchronously (apply directly).
    """
    if getattr(settings, "USE_CELERY", False):
        return task_func.delay(*args, **kwargs)  # async
    else:
        return task_func(*args, **kwargs)  # sync
