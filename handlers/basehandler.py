"""
All the Base Handlers needed by the server
"""

import webapp2
import json

__author__ = 'Lorenzo'


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
        return self.response.write(
            json.dumps({"error": 1, "status": code})
        ) if not exception else self.response.write(
            json.dumps({"error": 1, "status": code, "exception": exception})
        )
