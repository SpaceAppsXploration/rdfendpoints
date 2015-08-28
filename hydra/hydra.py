__author__ = 'lorenzo'

import webapp2

from flankers.errors import format_message
from config.config import _HYDRA


class HydraVocabulary(webapp2.RequestHandler):
    def get(self):
        """
        publish the HYDRA ApiDocumentation
        :return: Json
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/ld+json'
        api_doc = {} # to be implemented
        return self.response.write(api_doc)


class PublishContexts(webapp2.RequestHandler):
    def get(self, name):
        """
        publish contexts of the endpoints
        :param name: context name
        :return: Json
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/ld+json'
        self.response.headers['Access-Control-Expose-Headers'] = 'Link'
        self.response.headers['Link'] = '<' + _HYDRA + '>;rel="http://www.w3.org/ns/hydra/core#apiDocumentation'
        if name == 'EntryPoint':
            from hydra.contexts import EntryPoint
            return EntryPoint
        # only the entrypoint context is implemented
        # subsystems and components to come
        # return context based on name
        pass


class PublishEndpoints(webapp2.RequestHandler):
    def get(self, name=None, uuid=None):
        """
        publish EntryPoint, Collection and Resource JSON documents
        :return: Json
        """
        from flankers.tools import valid_uuid, families

        if not name:
            # return a hydra:EntryPoint > /rest/
            pass
        elif name == 'subsystems':
            if uuid and valid_uuid(uuid):
                # return a hydra:Resource component > /rest/components/<uuid>
                pass
            # return hydra:Collection
        elif name == 'components':
            if uuid and valid_uuid(uuid):
                # return a hydra:Resource subsystem family > /rest/subsystems/<uuid>
                pass
            # return hydra:Collection > /rest/subsystems
            pass

        self.response.status = 404
        return self.response.write(format_message('Wrong URL'))