__author__ = 'lorenzo'

from config.config import _HYDRA_VOCAB

EntryPoint = {
    "@context": {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": _HYDRA_VOCAB + "#",
        "EntryPoint": "vocab:EntryPoint",
        "subsystems": {
            "@id": "vocab:EntryPoint/subsystems",
            "@type": "@id",
            "hydra:method": "GET"
        },
        "register_component": {
            "@id": "vocab:EntryPoint/components",
            "@type": "@id",
            "hydra:method": "POST"
        }

    }
}

Collection = {
    "@context": {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": _HYDRA_VOCAB + "#",
        "Collection": "http://www.w3.org/ns/hydra/core#Collection",
        "members": "http://www.w3.org/ns/hydra/core#member"
    }
}

Subsystem = {
    "@context": {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": _HYDRA_VOCAB + "#",
        "Subsystem": "vocab:Subsystem",
        "name": "vocab:Subsystem/name",
        "is_open": "vocab:isOpen"
    }
}

Component = {
    "@context": {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": _HYDRA_VOCAB + "#",
        "Subsystem": "vocab:Component",
        "name": "vocab:Component/name",
        "is_open": "vocab:isOpen"
    }
}

ApiDocumentation = {
    "@context": {
        "vocab": _HYDRA_VOCAB + "#",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "ApiDocumentation": "hydra:ApiDocumentation",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedProperty": "hydra:supportedProperty",
        "supportedOperation": "hydra:supportedOperation",
        "method": "hydra:method",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "label": "rdfs:label",
        "description": "rdfs:comment",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        }
    },
    "@id": _HYDRA_VOCAB,
    "@type": "ApiDocumentation",
    "supportedClass": [
        {
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "hydra:title": "Resource",
            "hydra:description": None,
            "supportedOperation": [],
            "supportedProperty": []
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Collection",
            "@type": "hydra:Class",
            "hydra:title": "Collection",
            "hydra:description": None,
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "hydra:title": "members",
                    "hydra:description": "The members of this collection.",
                    "required": None,
                    "readonly": False,
                    "writeonly": False
                }
            ]
        },
        {
            "@id": "vocab:Component",
            "@type": "hydra:Class",
            "subClassOf": None,
            "label": "Component",
            "description": "A component in a spacecraft, belonging to a Subsystem",
        },
        {
            "@id": "vocab:Subsystem",
            "@type": "hydra:Class",
            "subClassOf": None,
            "label": "Subsystem",
            "description": "One or more components with the same function inside a spacecraft",
            "supportedProperty": [
                {
                    "property": {
                        "@id": "vocab:Subsystem/name",
                        "@type": "rdf:Property",
                        "label": "name",
                        "description": "The subsystem name",
                        "domain": "vocab:Subsystem",
                        "range": "http://www.w3.org/2001/XMLSchema#string",
                        "supportedOperation": []
                    },
                    "hydra:title": "name",
                    "hydra:description": "The subsystem name",
                    "required": None,
                    "readonly": False,
                    "writeonly": False
                }
            ]
        }
    ]
}