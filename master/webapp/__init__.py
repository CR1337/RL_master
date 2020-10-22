from flask import make_response
from flask_api import status
from functools import wraps
import sys


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception:
            exc_type, exc, _ = sys.exc_info()
            content = {
                'exception_type': str(exc_type),
                'exception_args': vars(exc)
            }
            status_code = status.HTTP_400_BAD_REQUEST
            response = make_response((content, status_code))
        finally:
            return response
    return wrapper
