__author__ = 'lorenzo'

from config.config import _REST_SERVICE, _SERVICE


def format_message(exception, root=_REST_SERVICE):
    if root == 'hydra':
        root = _SERVICE + '/hydra/'
    return str({"error": 1, "exception": exception, "back": root})
