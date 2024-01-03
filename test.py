import unittest
from io import StringIO

from celestial_body import CelestialBody
from solar_system_file import SolarSystemFile
from solar_system_error import SettingsFileError
from physics import Physics
from math import sqrt

class TestPhysics(unittest.TestCase):

    def test_abs_distance(self):
        a = CelestialBody("A", 12, 3, [-1,20,100], [0,0,0], [0,0,0])        
        b = CelestialBody("B", 34, 16, [12, 5, -7], [0,0,0], [0,0,0])

        physics = Physics()
        self.assertEqual(sqrt(11843), physics.abs_distance(a.get_position(), b.get_position()))
    
    def test_displacement(self):
        a = CelestialBody("A", 12, 3, [-1,20,100], [0,0,0], [0,0,0])        
        b = CelestialBody("B", 34, 16, [12, 5, -7], [0,0,0], [0,0,0])

        physics = Physics()
        self.assertEqual([13,-15,-107], physics.displacement(a.get_position(), b.get_position()))
    
    def test_grav_force(self):
        a = CelestialBody("A", 12, 3, [-1,20,100], [0,0,0], [0,0,0])        
        b = CelestialBody("B", 34, 16, [12, 5, -7], [0,0,0], [0,0,0])

        physics = Physics()
        expected = [1.611e-10,-1.210e-10,-2.378e-12]
        calculated = physics.gravitational_force(a.get_mass(), b.get_mass(), physics.displacement(a.get_position(), b.get_position()))
        for i in range(3):
            self.assertAlmostEqual(expected[i], calculated[i], 3)

class TestFileReader(unittest.TestCase):

    def test_read_settings_file(self):
        test_data = "Sun,1.989E30,696E6,0:0:0,0:0:0,255:255:0\n" + "Mercury,3.3E23,2439E3,57.9E9:0:0,0:47.39E3:0,186:169:145\n"

        self.test_file = StringIO(test_data)
        reader = SolarSystemFile()
        system = reader.read_settings_file(self.test_file)
        self.test_file.close()

        self.assertEqual(system.celestial_bodies[0].get_name(), 'Sun', "Wrong name!")
        self.assertEqual(system.celestial_bodies[1].get_name(), 'Mercury', "Wrong name!")
        self.assertEqual(system.get_body('Sun').get_colour(), [255,255,0], "Wrong colour!")
        self.assertEqual(system.get_body('Mercury').get_mass(), 3.3e23, "Wrong mass!")
        self.assertEqual(system.get_body('Mercury').get_position(), [57.9e9,0,0], "Wrong position")
        self.assertEqual(system.get_body('Mercury').get_velocity(), [0,47.39e3,0], "Wrong velocity")

    def test_same_position_file(self):
        test_data = "Sun,1.989E30,696E6,0:0:0,0:0:0,255:255:0\n" + "Mercury,3.3E23,2439E3,0:0:0,0:47.39E3:0,186:169:145\n"
        self.test_file = StringIO(test_data)
        reader = SolarSystemFile()
        try:
            system = reader.read_settings_file(self.test_file)
        except SettingsFileError:
            pass
        else:
            self.fail("Didn't catch exception.")
        self.test_file.close()
    
    def test_too_fast_file(self):
        test_data = "Sun,1.989E30,696E6,0:0:0,0:0:0,255:255:0\n" + "Mercury,3.3E23,2439E3,57.9E9:0:0,0:301E6:0,186:169:145\n"
        self.test_file = StringIO(test_data)
        reader = SolarSystemFile()
        try:
            system = reader.read_settings_file(self.test_file)
        except SettingsFileError:
            pass
        else:
            self.fail("Didn't catch exception.")
        self.test_file.close()
    
    def test_mixed_dimensions(self):
        test_data = "Sun,1.989E30,696E6,0:0,0:0:0,255:255:0\n" + "Mercury,3.3E23,2439E3,0:0:0,0:47.39E3:0,186:169:145\n"
        self.test_file = StringIO(test_data)
        reader = SolarSystemFile()
        try:
            system = reader.read_settings_file(self.test_file)
        except SettingsFileError:
            pass
        else:
            self.fail("Didn't catch exception.")
        self.test_file.close()
    
    def test_invalid_vector(self):
        test_data = "Sun,1.989E30,696E6,0:0:0,0:0:0,255:abc:0\n" + "Mercury,3.3E23,2439E3,0:0:0,0:47.39E3:0,186:169:145\n"
        self.test_file = StringIO(test_data)
        reader = SolarSystemFile()
        try:
            system = reader.read_settings_file(self.test_file)
        except SettingsFileError:
            pass
        else:
            self.fail("Didn't catch exception.")
        self.test_file.close()

if __name__ == '__main__':
    unittest.main()