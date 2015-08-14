"""
Technical constraints for different families/kinds of subsystems.
From these classes many instances can be generated, with quantities
generated from given intervals.
Aerospace support from Giacomo Gatto
"""

__author__ = 'lorenzo'

tech_constrains = dict({
    "communication" : {
        "slug": "COM",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
        "power": {"min": -200, "max": -1},
        "mass": {"min": 30, "max": 100},
        "cost": {"min": 1000, "max": 10000},
        "minWorkingTemp": { "min": -40, "max": -20 },
        "maxWorkingTemp": { "min": 40, "max": 90 }
    },
    "propulsion" : {
        "slug": "PROP",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
        "power": {"min": -200, "max": -50},
        "mass": {"min": 10, "max": 100},
        "cost": {"min": 5000, "max": 25000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "detector" : {
        "slug": "DTR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
        "sensor": ["ImagingDetector", "MassSpectrometer", "SpectroPhotometer", "SingleChannelPhotometer", "Radar",
                     "MultiChannelPhotometer", "MichelsonInterferometer", "FabryPerot", "DustDetectors"],
        "power": {"min": -100, "max": -10},
        "mass": {"min": 50, "max": 400},
        "cost": {"min": 2000, "max": 15000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "primary power" : {
        "slug": "PPW",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
        "power": {"min": 200, "max": 2000},
        "density" : 1.5,
        "mass": {"min": 30, "max": 100},
        "cost": {"min": 2000, "max": 10000},
        "minWorkingTemp": { "min": -60, "max": -40 },
        "maxWorkingTemp": { "min": 50, "max": 100 }
    },
    "backup power" : {
        "slug": "BCK",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
        "power": {"min": 50, "max": 1500},
        "density": 2,
        "mass": {"min": 100, "max": 300},
        "cost": {"min": 5000, "max": 25000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "thermal" : {
        "slug": "THR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
        "power": {"min": -100, "max": 100},
        "mass": {"min": 20, "max": 150},
        "cost": {"min": 500, "max": 4000},
        "minTemperature": { "min": -100, "max": -30 },
        "maxTemperature": { "min": 50, "max": 100 }
    },
    "structure" : {
        "slug": "STR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
        "mass": {"min": 10, "max": 100},
        "cost": {"min": 2000, "max": 35000},
        "minWorkingTemp": { "min": -90, "max": -30 },
        "maxWorkingTemp": { "min": 30, "max": 70 }
    },
    "command and data" : {
        "slug": "CDH",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
        "power": {"min": -50, "max": -5},
        "mass": {"min": 20, "max": 70},
        "cost": {"min": 1000, "max": 5000},
        "minWorkingTemp": { "min": -20, "max": -10 },
        "maxWorkingTemp": { "min": 10, "max": 50 }
    },
    "attitude and orbit control" : {
        "slug": "AODCS",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
        "power": {"min": -150, "max": 100},
        "mass": {"min": 10, "max": 80},
        "cost": {"min": 1000, "max": 15000},
        "minWorkingTemp": { "min": -50, "max": -30 },
        "maxWorkingTemp": { "min": 30, "max": 70 },
        "active": ["magnetic torque", "cold gas", "microthrusters"],
        "passive": ["rotation", "gravity", "solar pressure"]
    }
})
