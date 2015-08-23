import json

component = json.dumps({
    "http://ontology.projectchronos.eu/subsystems/name": "138KV detector",
    "http://ontology.projectchronos.eu/subsystems/minWorkingTemp": {
        "@type": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius",
        "@value": -28
    },
    "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue": {
        "@type": "http://sw.opencyc.org/2012/05/10/concept/en/Euro",
        "@value": 14042
    },
    "http://ontology.projectchronos.eu/subsystems/holdsSensor": "http://ontology.projectchronos.eu/subsystems/FabryPerot",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#label": "e3349c8fe32d4174a405aeee1e441fad",
    "http://ontology.projectchronos.eu/subsystems/hasVolume": {
        "@type": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
        "@value": 182
    },
    "http://ontology.projectchronos.eu/subsystems/hasMass": {
        "@type": "http://sw.opencyc.org/2012/05/10/concept/en/Gram",
        "@value": 186
    },
    "http://ontology.projectchronos.eu/subsystems/maxWorkingTemp": {
        "@type": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius",
        "@value": 58
    },
    "http://ontology.projectchronos.eu/sensors/hasFieldOfResearch": "http://ontology.projectchronos.eu/sensors/EarthObservation",
    "http://ontology.projectchronos.eu/subsystems/isStandard": "Cubesat",
    "http://ontology.projectchronos.eu/subsystems/manufacturer": "Chronos",
    "uuid": "eef243a533f34483859b7bd736b5563d",
    "@type": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
    "http://ontology.projectchronos.eu/subsystems/hasPower": {
        "@type": "http://dbpedia.org/data/Watt.ntriples",
        "@value": -98
    }
})