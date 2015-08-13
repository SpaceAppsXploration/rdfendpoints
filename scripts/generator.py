import random


def random_value(interval):
    """
    Generates a random integer value from a given interval
    """
    if not isinstance(interval, dict):
        raise ValueError('value has to be dict')
    return random.randrange(interval['min'], interval['max'], 1) // 1


def linear_function():
    pass


def generate_object(name, subsystem):
    """
    Generates random components from given input dictionary
    """
    result = {}
    result['subsystems:hasMass'] = random_value(subsystem['mass'])
    result['linked'] = subsystem['ontology']
    result['kind'] = name

    # if it is a detector, defines what kind of sensor it holds
    if 'sensor' in subsystem.keys(): result['sensor'] = random.choice(subsystem['sensor'])

    # general rule for most of the subsystems families
    if 'minWorkingTemp' in subsystem.keys() and subsystem['slug'] != 'THR':
        if not name == 'structure':
            result['subsystems:hasPower'] = random_value(subsystem['power'])
        result['subsystems:minWorkingTemp'] = random_value(subsystem['minWorkingTemp'])
        result['subsystems:maxWorkingTemp'] = random_value(subsystem['maxWorkingTemp'])

        # rule for primary power or backup
        if 'density' in subsystem.keys():
            result['subsystems:hasVolume'] = int(result['subsystems:hasMass'] / subsystem['density']) // 1        
            if name == 'primary power':
                result['subsystems:hasMonetaryValue'] = result['subsystems:hasPower'] * 5
                return result
            elif name == 'backup power':
                result['subsystems:hasMonetaryValue'] = result['subsystems:hasPower'] * 16
                return result
        else:    # rule for other not generator
            result['subsystems:hasVolume'] = result['subsystems:hasMass'] + random_value({'min': -5, 'max': 5})
            if name not in ['structure', 'attitude and orbit control']:
                result['subsystems:hasMonetaryValue'] = random_value(subsystem['cost'])
                return result
            else:
                if name == 'structure':
                    result['subsystems:hasPower'] = 0  
                    result['subsystems:hasMonetaryValue'] = int(350000 / result['subsystems:hasMass']) // 1
                    return result
                elif name == 'attitude and orbit control':
                    if result['subsystems:hasPower'] > 0:
                        result['subsystems:hasPower'] = 0 
                        result['type'] = 'passive'
                        result['mechanism'] = random.choice(subsystem['passive'])
                    else:
                        result['type'] = 'active'
                        result['mechanism'] = random.choice(subsystem['active'])
                    result['subsystems:hasMonetaryValue'] = random_value(subsystem['cost'])
                    return result
    # exclusive rule for thermal family of subsystems
    else:
        result['subsystems:hasVolume'] = result['subsystems:hasMass'] + random_value({'min': -5, 'max': 5})
        result['subsystems:hasPower'] = random_value(subsystem['power'])
        if result['subsystems:hasPower'] > 0 : result['subsystems:hasPower'] = 0 
        result['subsystems:minWorkingTemp'] = random_value(subsystem['minTemperature'])
        result['subsystems:maxWorkingTemp'] = random_value(subsystem['maxTemperature'])

        result['subsystems:hasMonetaryValue'] = (result['subsystems:maxWorkingTemp'] - result['subsystems:minWorkingTemp']) * 20

        if result['subsystems:hasPower'] == 0:
            result['type'] = 'passive'
        else:
            result['type'] = 'active'
        return result




            



