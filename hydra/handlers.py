__author__ = 'lorenzo'

import webapp2
import json

from flankers.errors import format_message
from config.config import _HYDRA_VOCAB, _SERVICE

_CONTENT_TYPE = 'application/ld+json'


class HydraVocabulary(webapp2.RequestHandler):
    def get(self):
        """
        publish the HYDRA ApiDocumentation vocabulary
        :return: Json
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = _CONTENT_TYPE
        self.response.headers['Access-Control-Expose-Headers'] = 'Link'
        self.response.headers['Link'] = '<' + _HYDRA_VOCAB + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
        from contexts import ApiDocumentation
        return self.response.write(json.dumps(ApiDocumentation, indent=2))


class PublishContexts(webapp2.RequestHandler):
    def get(self, name):
        """
        publish contexts of the endpoints
        :param name: context name
        :return: Json
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = _CONTENT_TYPE
        self.response.headers['Access-Control-Expose-Headers'] = 'Link'
        self.response.headers['Link'] = '<' + _HYDRA_VOCAB + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
        import contexts
        print type(dir(contexts))
        if name in dir(contexts) and not name.startswith('_'):
            # load the right variable in the 'contexts' module
            self.response.status = 200
            return self.response.write(json.dumps(getattr(contexts, name), indent=2))
        # return context based on name
        self.response.status = 404
        return self.response.write(
            format_message('/hydra/contexts/ GET: wrong context name', root='hydra')
        )


class PublishEndpoints(webapp2.RequestHandler):
    def get(self, name=None):
        """
        publish EntryPoint, Collection and Resource JSON documents
        :return: Json
        """
        from flankers.tools import valid_uuid, families

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = _CONTENT_TYPE
        self.response.headers['Access-Control-Expose-Headers'] = 'Link'
        self.response.headers['Link'] = '<' + _HYDRA_VOCAB + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'

        if not name:
            # return a hydra:EntryPoint > GET: /hydra/spacecraft/
            self.response.status = 200
            return self.response.write(json.dumps({
                "@context": _SERVICE + "/hydra/contexts/EntryPoint",
                "@id": _SERVICE + "/hydra/spacecraft/",
                "@type": "EntryPoint",
                "go_to_subsystems": _SERVICE + "/hydra/spacecraft/subsystems",
                "register_component": "under-construction"
            }, indent=2))
            pass
        elif name == 'subsystems':
            uuid = self.request.get('uuid')
            if uuid and uuid in families:
                # return a hydra:Resource component > GET: /hydra/spacecraft/subsystems?uuid=<uuid>
                result = {
                    "@context": _SERVICE + "/hydra/contexts/Subsystem",
                    "@id": _SERVICE + "/hydra/spacecraft/subsystems?uuid={}".format(uuid),
                    "@type": "Subsystem",
                    "name": uuid,
                    "application/n-triples": "http://ontology.projectchronos.eu/subsystems/{}".format(uuid),
                    "go_to_components": _SERVICE + "/hydra/spacecraft/components?uuid={}".format(uuid),
                    "application/ld+json": "http://ontology.projectchronos.eu/subsystems/{}/?format=jsonld".format(uuid),
                    "is_open": True,

                }
                return self.response.write(json.dumps(result, indent=2))
            # return hydra:Collection
            results = {
                "@context": _SERVICE + "/hydra/contexts/Collection",
                "@type": "Collection",
                "@id": _SERVICE + "/hydra/spacecraft/subsystems",
                "members": []
            }
            [results["members"].append({
                "@id": _SERVICE + "/hydra/spacecraft/subsystems?uuid={}".format(f),
                "@type": "vocab:Subsystem"})
                for f in families]
            self.response.status = 200
            return self.response.write(json.dumps(results, indent=2))

        elif name == 'components':
            uuid = self.request.get('uuid')
            if uuid and valid_uuid(uuid):
                # return a hydra:Resource component > /hydra/spacecraft/components?uuid=<uuid>
                try:
                    from datastore.models import Component
                    body = Component.parse_to_jsonld(uuid)
                except ValueError as e:
                    return self.response.write(format_message(e))
                return self.response.write(body)
            elif uuid in families:
                # return hydra:Collection components by family > /hydra/spacecraft/components?uuid=<subsystem_name>
                from datastore.models import Component
                body = Component.hydrafy(Component.get_by_collection(uuid))
                return self.response.write(body)
            # return hydra:Collection > /hydra/spacecraft/subsystems
            self.response.status = 404
            return self.response.write(
                format_message('/hydra/spacecraft/components/ GET: needs a "uuid" parameter to be specified; it can be an hex or a subsystem-name', root='hydra')
            )

        self.response.status = 404
        return self.response.write(
            format_message('Wrong URL', root='hydra')
        )