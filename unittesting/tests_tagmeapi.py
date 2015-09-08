__author__ = 'lorenzo'

import unittest
from flankers.tagmeapi.tagMeService import TagMeService


class tagmeapiTest(unittest.TestCase):
    """
    Test TagMeApi interface
    """
    def setUp(self):
        # list of texts
        self.test1 = ["""
        Functional Extravehicular Mobility Units (EMUs) with high precision gloves are essential for the success of Extravehicular Activity (EVA).
        """, """
        The NASA Protoflight Research Initiative is an internal NASA study conducted within the Office of the Chief Engineer to better understand the use of Protoflight within NASA. Extensive literature reviews and interviews with key NASA members with experience in both robotic and human spaceflight missions has resulted in three main conclusions and two observations. The first conclusion is that NASA's Protoflight method is not considered to be "prescriptive." The current policies and guidance allo...
        """, """
        Two university student teams from ESAs Spin Your Thesis! programme have recently published valuable results in scientific journals. One study reveals a clear effect on the electrical behaviour of plant cells. The other offers a way to stimulate bone cells formation.
        """]

        # BDpedia categories that are related to the subject
        self.scopes = TagMeService.return_gen_scopes()


class tagmeapiSpotTest(tagmeapiTest):
    def runTest(self):
        """
        test the spotting service for a test string
        """
        print '<SPOTTING API>'
        for i, t in enumerate(self.test1):
            results = TagMeService.check_spotting(t)
            print i, [s['spot'] for s in results['value']['spots']]
            if results['spotted']:
                if i == 0:
                    expected = [u'Functional', u'Mobility', u'Units', u'EMUs', u'high', u'precision', u'gloves',
                                u'essential', u'success', u'Extravehicular Activity', u'EVA']
                    assert [s['spot'] for s in results['value']['spots']] == expected
                elif i == 1:
                    expected = [u'NASA', u'Research', u'Initiative', u'internal', u'study', u'conducted', u'Office', u'Chief Engineer', u'Engineer', u'understand', u'literature reviews', u'interviews', u'key', u'members', u'experience', u'robotic', u'human spaceflight', u'missions', u'main', u'observations', u'first', u'conclusion', u"NASA's", u'method', u'prescriptive', u'The current', u'policies', u'guidance', u'allo']
                    assert [s['spot'] for s in results['value']['spots']] == expected
                elif i == 2:
                    expected = [u'university', u'university student', u'student', u'teams', u'ESAs', u'Spin', u'Thesis', u'programme', u'published', u'scientific journals', u'study', u'clear', u'electrical', u'behaviour', u'plant', u'plant cells', u'way', u'stimulate', u'bone cells', u'formation']
                    assert [s['spot'] for s in results['value']['spots']] == expected
                else:
                    assert False


class tagmeapiTagTest(tagmeapiTest):
    def runTest(self):
        """
        test the tagging service for any given term spotted
        """
        from flankers.textsemantics import return_wikipedia_term
        print '<TAGGING API>'
        for i, t in enumerate(self.test1):
            response = TagMeService.check_spotting(t)
            results = return_wikipedia_term(response)
            print i, results
            if i == 0:
                expected = [u'Functional_(mathematics)', u'Electron_mobility', u'Units_of_measurement', u'Electric_multiple_unit', u'High,_Just-As-High,_and_Third', u'Accuracy_and_precision', u'Glove', u'Essential_Marvel', u'Success_(company)', u'Extra-vehicular_activity', u'Extra-vehicular_activity']
                assert results == expected
            elif i == 1:
                expected = [u'NASA', u'Research', u'Initiative', u'Neijia', u'Research', u'Conducting', u'The_Office_(U.S._TV_series)', u'Engineer', u'Engineer', u'Engineer', u'Understanding', u'Literature_review', u'Interview', u'Key_(music)', u'Member_of_Parliament', u'Experience', u'Robotics', u'Human_spaceflight', u'Mission_(Christianity)', u'Main_(river)', u'Observation', u'World_War_I', u'Entailment', u'NASA', u'Method_(computer_programming)', u'Linguistic_prescription', u'The_Current_(song)', u'Policy', u'Missile_guidance', u'Emic_unit']
                assert results == expected
            elif i == 2:
                expected = [u'University', u'University', u'Student', u'Student', u'Student', u'List_of_Champ_Car_teams', u'Exploration_Systems_Architecture_Study', u'Spin_(magazine)', u'Thesis', u'Television_program', u'Video_game_publisher', u'Scientific_journal', u'Research', u'Clear_(Scientology)', u'Electricity', u'Behavior', u'Plant', u'Plant', u'Plant_cell', u'Cell_(biology)', u'By_the_Way', u'Stimulation', u'Bone_cell', u'Formation_(stratigraphy)']
                assert results == expected
            else:
                assert False


class tagmeapiRelateTest(tagmeapiTest):
    def runTest(self):
        """
        test the relating service for terms in relation with generic scopes
        """
        for i, t in enumerate(self.test1):
            print '<RELATING API>'
            results = []
            for spot in [s['spot'] for s in TagMeService.check_spotting(t)['value']['spots']]:
                result = TagMeService.retrieve_taggings(spot.encode('utf-8'), method='POST')
                for n in result['annotations']:
                    title = n['title'].replace(' ', '_')  # strip whitespaces from dbpedia tag
                    results.append(TagMeService.relate(title, self.scopes))  # compare the spotted and tagged term to the generic scopes
            print i, results
            # 'couple' are the two wikipedia terms been checked, 'rel' is the correlation index (rho). The more the rho
            # is closer to 0.5 the more the terms are related. The standard interval of relevance is 0.42 < rho < 0.61
            if i == 0:
                expected = [[{u'couple': u'Functional_(mathematics) Physics', u'rel': u'0.4235'}], [{u'couple': u'Electron_mobility Cosmic_ray', u'rel': u'0.4784'}], [{u'couple': u'Units_of_measurement Astrophysics', u'rel': u'0.4353'}, {u'couple': u'Units_of_measurement Geodesy', u'rel': u'0.5333'}, {u'couple': u'Units_of_measurement Astronomical_object', u'rel': u'0.4824'}, {u'couple': u'Units_of_measurement Astronomy', u'rel': u'0.4824'}, {u'couple': u'Units_of_measurement Navigation', u'rel': u'0.4706'}, {u'couple': u'Units_of_measurement Physics', u'rel': u'0.4275'}, {u'couple': u'Units_of_measurement Planetary_science', u'rel': u'0.4275'}], [], [], [{u'couple': u'Accuracy_and_precision Geodesy', u'rel': u'0.5176'}, {u'couple': u'Accuracy_and_precision Astronomical_object', u'rel': u'0.4471'}, {u'couple': u'Accuracy_and_precision Navigation', u'rel': u'0.4745'}], [], [], [], [{u'couple': u'Extra-vehicular_activity Aerospace', u'rel': u'0.4392'}, {u'couple': u'Extra-vehicular_activity Astrophysics', u'rel': u'0.4471'}, {u'couple': u'Extra-vehicular_activity Cosmic_ray', u'rel': u'0.5804'}, {u'couple': u'Extra-vehicular_activity Spaceflight', u'rel': u'0.8353'}, {u'couple': u'Extra-vehicular_activity Spacecraft', u'rel': u'0.7059'}, {u'couple': u'Extra-vehicular_activity Geodesy', u'rel': u'0.5137'}, {u'couple': u'Extra-vehicular_activity Astronomical_object', u'rel': u'0.5137'}, {u'couple': u'Extra-vehicular_activity Aircraft', u'rel': u'0.4235'}, {u'couple': u'Extra-vehicular_activity Atmosphere', u'rel': u'0.4784'}, {u'couple': u'Extra-vehicular_activity Navigation', u'rel': u'0.4941'}, {u'couple': u'Extra-vehicular_activity Satellite', u'rel': u'0.6941'}, {u'couple': u'Extra-vehicular_activity Spaceflight', u'rel': u'0.8353'}, {u'couple': u'Extra-vehicular_activity NASA', u'rel': u'0.6000'}], [{u'couple': u'Extra-vehicular_activity Aerospace', u'rel': u'0.4392'}, {u'couple': u'Extra-vehicular_activity Astrophysics', u'rel': u'0.4471'}, {u'couple': u'Extra-vehicular_activity Cosmic_ray', u'rel': u'0.5804'}, {u'couple': u'Extra-vehicular_activity Spaceflight', u'rel': u'0.8353'}, {u'couple': u'Extra-vehicular_activity Spacecraft', u'rel': u'0.7059'}, {u'couple': u'Extra-vehicular_activity Geodesy', u'rel': u'0.5137'}, {u'couple': u'Extra-vehicular_activity Astronomical_object', u'rel': u'0.5137'}, {u'couple': u'Extra-vehicular_activity Aircraft', u'rel': u'0.4235'}, {u'couple': u'Extra-vehicular_activity Atmosphere', u'rel': u'0.4784'}, {u'couple': u'Extra-vehicular_activity Navigation', u'rel': u'0.4941'}, {u'couple': u'Extra-vehicular_activity Satellite', u'rel': u'0.6941'}, {u'couple': u'Extra-vehicular_activity Spaceflight', u'rel': u'0.8353'}, {u'couple': u'Extra-vehicular_activity NASA', u'rel': u'0.6000'}]]
                assert results == expected
            elif i == 1:
                expected = [[{u'couple': u'NASA Astrophysics', u'rel': u'0.4549'}, {u'couple': u'NASA Cosmic_ray', u'rel': u'0.4745'}, {u'couple': u'NASA Spaceflight', u'rel': u'0.5765'}, {u'couple': u'NASA Spacecraft', u'rel': u'0.5569'}, {u'couple': u'NASA Astronomical_object', u'rel': u'0.4471'}, {u'couple': u'NASA Astronomy', u'rel': u'0.4510'}, {u'couple': u'NASA Atmosphere', u'rel': u'0.4863'}, {u'couple': u'NASA Satellite', u'rel': u'0.5451'}, {u'couple': u'NASA Spaceflight', u'rel': u'0.5765'}, {u'couple': u'NASA Planetary_science', u'rel': u'0.4588'}], [{u'couple': u'Research Physics', u'rel': u'0.4431'}], [], [], [{u'couple': u'Research Physics', u'rel': u'0.4431'}], [], [], [], [], [], [], [], [], [], [], [{u'couple': u'Experience Navigation', u'rel': u'0.4275'}], [{u'couple': u'Robotics Aerospace', u'rel': u'0.5255'}, {u'couple': u'Robotics Astrophysics', u'rel': u'0.5608'}, {u'couple': u'Robotics Spaceflight', u'rel': u'0.4667'}, {u'couple': u'Robotics Spacecraft', u'rel': u'0.4863'}, {u'couple': u'Robotics Geodesy', u'rel': u'0.5882'}, {u'couple': u'Robotics Astronomy', u'rel': u'0.4706'}, {u'couple': u'Robotics Spaceflight', u'rel': u'0.4667'}, {u'couple': u'Robotics Physics', u'rel': u'0.4549'}, {u'couple': u'Robotics Planetary_science', u'rel': u'0.5843'}], [{u'couple': u'Human_spaceflight Aerospace', u'rel': u'0.4471'}, {u'couple': u'Human_spaceflight Astrophysics', u'rel': u'0.4706'}, {u'couple': u'Human_spaceflight Cosmic_ray', u'rel': u'0.6039'}, {u'couple': u'Human_spaceflight Spaceflight', u'rel': u'0.8392'}, {u'couple': u'Human_spaceflight Spacecraft', u'rel': u'0.7333'}, {u'couple': u'Human_spaceflight Avionics', u'rel': u'0.5216'}, {u'couple': u'Human_spaceflight Geodesy', u'rel': u'0.5020'}, {u'couple': u'Human_spaceflight Astronomical_object', u'rel': u'0.5412'}, {u'couple': u'Human_spaceflight Astronomy', u'rel': u'0.4275'}, {u'couple': u'Human_spaceflight Atmosphere', u'rel': u'0.5333'}, {u'couple': u'Human_spaceflight Navigation', u'rel': u'0.4510'}, {u'couple': u'Human_spaceflight Satellite', u'rel': u'0.7137'}, {u'couple': u'Human_spaceflight Spaceflight', u'rel': u'0.8392'}, {u'couple': u'Human_spaceflight NASA', u'rel': u'0.5922'}, {u'couple': u'Human_spaceflight Planetary_science', u'rel': u'0.4471'}], [], [], [{u'couple': u'Observation Astrophysics', u'rel': u'0.5451'}, {u'couple': u'Observation Geodesy', u'rel': u'0.5569'}, {u'couple': u'Observation Astronomical_object', u'rel': u'0.5725'}, {u'couple': u'Observation Astronomy', u'rel': u'0.5059'}, {u'couple': u'Observation Atmosphere', u'rel': u'0.4392'}, {u'couple': u'Observation Physics', u'rel': u'0.4824'}, {u'couple': u'Observation Planetary_science', u'rel': u'0.5490'}], [], [], [{u'couple': u'NASA Astrophysics', u'rel': u'0.4549'}, {u'couple': u'NASA Cosmic_ray', u'rel': u'0.4745'}, {u'couple': u'NASA Spaceflight', u'rel': u'0.5765'}, {u'couple': u'NASA Spacecraft', u'rel': u'0.5569'}, {u'couple': u'NASA Astronomical_object', u'rel': u'0.4471'}, {u'couple': u'NASA Astronomy', u'rel': u'0.4510'}, {u'couple': u'NASA Atmosphere', u'rel': u'0.4863'}, {u'couple': u'NASA Satellite', u'rel': u'0.5451'}, {u'couple': u'NASA Spaceflight', u'rel': u'0.5765'}, {u'couple': u'NASA Planetary_science', u'rel': u'0.4588'}], [], [], [], [], [{u'couple': u'Missile_guidance Spaceflight', u'rel': u'0.4235'}, {u'couple': u'Missile_guidance Avionics', u'rel': u'0.4549'}, {u'couple': u'Missile_guidance Command_and_control', u'rel': u'0.4510'}, {u'couple': u'Missile_guidance Spaceflight', u'rel': u'0.4235'}], []]
                assert results == expected
            elif i == 2:
                expected = [[{u'couple': u'University Physics', u'rel': u'0.4235'}], [{u'couple': u'University Physics', u'rel': u'0.4235'}], [], [], [], [], [{u'couple': u'Exploration_Systems_Architecture_Study Cosmic_ray', u'rel': u'0.4588'}, {u'couple': u'Exploration_Systems_Architecture_Study Spaceflight', u'rel': u'0.4863'}, {u'couple': u'Exploration_Systems_Architecture_Study Spacecraft', u'rel': u'0.5412'}, {u'couple': u'Exploration_Systems_Architecture_Study Avionics', u'rel': u'0.5059'}, {u'couple': u'Exploration_Systems_Architecture_Study Spaceflight', u'rel': u'0.4863'}, {u'couple': u'Exploration_Systems_Architecture_Study NASA', u'rel': u'0.4667'}], [], [], [], [], [{u'couple': u'Scientific_journal Astrophysics', u'rel': u'0.4706'}, {u'couple': u'Scientific_journal Astronomy', u'rel': u'0.4314'}, {u'couple': u'Scientific_journal Physics', u'rel': u'0.4510'}, {u'couple': u'Scientific_journal Planetary_science', u'rel': u'0.4314'}], [{u'couple': u'Research Physics', u'rel': u'0.4431'}], [], [{u'couple': u'Electricity Astrophysics', u'rel': u'0.4275'}, {u'couple': u'Electricity Physics', u'rel': u'0.4627'}], [], [], [], [{u'couple': u'Plant_cell Atmosphere', u'rel': u'0.5020'}], [], [], [], [], []]
                assert results == expected
            else:
                assert False


class tagmeapiCheckTest(tagmeapiTest):
    def runTest(self):
        """
        test the function that checks if any term has a proper correlation with the aerospace/astronomy/physics
        """
        for i, t in enumerate(self.test1):
            print '<CHECK IF TERMS are related to SPACEKNOWLEDGE>'
            results = []
            for spot in [s['spot'] for s in TagMeService.check_spotting(t)['value']['spots']]:
                result = TagMeService.retrieve_taggings(spot.encode('utf-8'), method='POST')
                for n in result['annotations']:
                    title = n['title'].replace(' ', '_')  # strip whitespaces from dbpedia tag
                    relate = TagMeService.relate(title, self.scopes)  # compare the spotted and tagged term to the generic scopes
                    results.append(TagMeService.check_if_rho_fits_spaceknowledge(relate))
            print i, results
            # print True, name and the mean of the rho of the term in relation with the scopes
            if i == 0:
                expected = [(True, u'Functional_(mathematics)', 0.4235), (True, u'Electron_mobility', 0.4784), (True, u'Units_of_measurement', 0.46557142857142864), False, False, (True, u'Accuracy_and_precision', 0.4797333333333333), False, False, False, (True, u'Extra-vehicular_activity', 0.5815923076923076), (True, u'Extra-vehicular_activity', 0.5815923076923076)]
                assert results == expected
            elif i == 1:
                expected = [(True, u'NASA', 0.5027600000000001), (True, u'Research', 0.4431), False, False, (True, u'Research', 0.4431), False, False, False, False, False, False, False, False, False, False, (True, u'Experience', 0.4275), (True, u'Robotics', 0.5115555555555555), (True, u'Human_spaceflight', 0.5775266666666666), False, False, (True, u'Observation', 0.5215714285714286), False, False, (True, u'NASA', 0.5027600000000001), False, False, False, False, (True, u'Missile_guidance', 0.43822500000000003), False]
                assert results == expected
            elif i == 2:
                expected = [(True, u'University', 0.4235), (True, u'University', 0.4235), False, False, False, False, (True, u'Exploration_Systems_Architecture_Study', 0.4908666666666666), False, False, False, False, (True, u'Scientific_journal', 0.4461), (True, u'Research', 0.4431), False, (True, u'Electricity', 0.4451), False, False, False, (True, u'Plant_cell', 0.502), False, False, False, False, False]
                assert results == expected
            else:
                assert False


class tagmeapiLabelsTest(tagmeapiTest):
    def runTest(self):
        """
        test the function that returns tagged labels from a given text
        """
        from flankers.textsemantics import find_related_concepts

        for i, t in enumerate(self.test1):
            results = find_related_concepts(t)
            print i, results
            # print True, name and the mean of the rho of the term in relation with the scopes
            if i == 0:
                expected = {'electric power units (electrical design)', 'precision time and time interval (ptti)',
                            'electric power units (aircraft)', 'auxiliary power units (apu) (aircraft)',
                            'electric power units (spacecraft)', 'manned maneuvering units',
                            'auxiliary power units (apu) (spacecraft)', 'extravehicular activity (eva) (operations)',
                            'extravehicular activity (eva) (equipment)',
                            'inertial sensors and measurement units (spacecraft)',
                            'inertial sensors and measurement units (aircraft)',
                            'extravehicular activity (physiological effects)'}
                assert results == expected
            elif i == 1:
                expected = {'robotics (hardware)', 'asteroids (observation)', 'robotics',
                            'extrasolar planets (observation)', 'snow and ice observations',
                            'remote manipulator arms (robotics)', 'moons (observation)', 'binaries (observation)',
                            'quasars (observation)', 'novae (observation)', 'celestial bodies (observation)',
                            'manned spacecraft', 'nebulae (observation)', 'black holes (observation)',
                            'manned orbital laboratories', 'supernovae (observation)', 'meteoroids (observation)',
                            'celestial motion (observation)', 'manned lunar exploration',
                            'histories of aeronautics and space programs', 'comets (observation)',
                            'manned planetary exploration', 'manned maneuvering units',
                            'appropriations hearings (nasa)', 'star trackers (observation)', 'pulsars (observation)',
                            'stars (observation)', 'galaxies (observation)', 'space programs',
                            'legal liability of manned space flight', 'meteors (observation)',
                            'scene analysis (robotics)', 'rendezvous guidance', 'manned flights (space exploration)',
                            'natural satellites (observation)', 'teleoperators (robotics)',
                            'observation of celestial bodies'}
                assert results == expected
            elif i == 2:
                expected = set([])
                assert results == expected
            else:
                assert False




if __name__ == '__main__':
    unittest.main()
