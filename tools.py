"""
Generic tools for handlers operations
"""

__author__ = 'lorenzo'

# from google.appengine.api import urlfetch

families = ['Spacecraft_Detector', 'Spacecraft_Propulsion', 'Spacecraft_PrimaryPower',
            'Spacecraft_BackupPower', 'Spacecraft_Thermal', 'Spacecraft_Structure', 'Spacecraft_CDH',
            'Spacecraft_Communication', 'Spacecraft_AODCS']


def valid_uuid(uuid):
    """
    matches if a string is a valid uuid.hex
    :param uuid:
    :return:
    """
    import re
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)

