__author__ = 'lorenzo'

from config.config import _HYDRA

EntryPoint = {
    "@context": {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": _HYDRA + "#",
        "EntryPoint": "vocab:EntryPoint",
        "subsystems": {
            "@id": "vocab:EntryPoint/subsystems",
            "@type": "@id"
        },
        "components": {
            "@id": "vocab:EntryPoint/components",
            "@type": "@id"
        },
        "register_component": {
            "@id": "vocab:EntryPoint/components",
            "@type": "@id"
        }

    }
}
