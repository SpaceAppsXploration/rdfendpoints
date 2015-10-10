"""
All the Base Handlers needed by the server
"""

import webapp2
import json

from config.config import _PATH

__author__ = 'Lorenzo'


class BaseHandler(webapp2.RequestHandler):
    """def handle_exception(self, exception, debug):
        import os
        from google.appengine.ext.webapp import template
        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

        path = os.path.join(_PATH, 'over_quota.html')
        return self.response.out.write(template.render(path, {}))
    """
    pass

class JSONBaseHandler(webapp2.RequestHandler):
    """
    Extends RequestHandler with new custom methods
    """
    def json_error_handler(self, code, exception=None):
        """
        Print out error in JSON format.
        :param code: status code to display (int)
        :param exception: error message
        :return: Display a JSON as response
        """
        self.response.status = code
        return json.dumps(
            {"error": 1, "status": code}
        ) if not exception else json.dumps(
            {"error": 1, "status": code, "exception": exception}
        )
