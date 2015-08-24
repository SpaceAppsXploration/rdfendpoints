__author__ = 'lorenzo'

from config import _REST_SERVICE


def format_message(exception):
    return str({"error": 1, "exception": exception, "back": _REST_SERVICE})
