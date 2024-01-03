from solar_system import SolarSystem
from celestial_body import CelestialBody
from solar_system_error import SettingsFileError
from physics import DIMENSION, LIGHTSPEED, Physics
from random import randrange

class SolarSystemFile:

    def read_settings_file(self, file):
        """
        Reads the settings file and returns the solar system object created based on it.
        """

        physics = Physics()
        system = SolarSystem()

        for orig_line in file:
            line = orig_line.split(',')
            if len(line) < 5 or len(line) > 6:
                raise SettingsFileError("Line '{}' has wrong amount of arguments".format(orig_line))

            # Read name, mass and radius
            name = line[0]
            try:
                mass = float(line[1])
                radius = float(line[2])
            except ValueError:
                raise SettingsFileError("Object {} mass {} or radius {} not a number.".format(name, line[1], line[2]))

            # Reads initial position, initial velocity and RGB-colour into vectors
            if len(line) == 6:
                vectors = [line[3].split(':'), line[4].split(':'), line[5].split(':')]
                if len(vectors[2]) != 3:
                    raise SettingsFileError("Invalid RGB-colour value: {}".format(vectors[2]))
            else:
                # If a colour has not been set, the planet is given a randomised colour.
                colour = [randrange(256) for i in range(3)]
                vectors = [line[3].split(':'), line[4].split(':'), colour]

            try:
                for i in range(len(vectors)):
                    for j in range(len(vectors[i])):
                        if i == 2:
                            vectors[i][j] = int(vectors[i][j])      # RGB-values are integers
                        else:
                            vectors[i][j] = float(vectors[i][j])
            except ValueError:
                raise SettingsFileError("Position, velocity or colour not numerical values")

            position, velocity, colour = vectors[0], vectors[1], vectors[2]
            if len(position) != DIMENSION or len(velocity) != DIMENSION:
                raise SettingsFileError("Position: {} or velocity: {} is wrong dimension".format(position, velocity))
            
            # Create the read body
            body = CelestialBody(name, mass, radius, position, velocity, colour)
            if physics.speed(body) >= LIGHTSPEED:
                raise SettingsFileError("Speed of body ({}) more than speed of light.".format(physics.speed(body)))

            # Add to system and check that it doesn't overlap with another body
            system.add_to_system(body)
            system.check_impact()
            if system.impact == True:
                raise SettingsFileError("2 bodies too close to each other.")
        
        system.set_size(self.determine_system_size(system))

        # Calculate the initial accelerations for all bodies
        for body in system.get_all_bodies():
            sigma_f = physics.net_force(body, system.get_all_bodies())
            a = physics.acceleration(sigma_f, body.get_mass())
            body.update_acceleration(a)
        # Save the initial state of the system
        system.save_state()

        return system
    
    def determine_system_size(self, system):
        """
        Given the list of celestial bodies, determines the size of the solar system, which is a cube 75 % larger than the distance of the furthest object from the origin (sun).
        """
        max_distance = [0 for i in range(DIMENSION)]
        for body in system.get_all_bodies():
            pos = body.get_position()
            for i in range(DIMENSION):
                if abs(pos[i]) > max_distance[i]:
                    max_distance[i] = abs(pos[i])
        system_size_max = [1.75*max_distance[i] for i in range(DIMENSION)]
        system_size_max = max(system_size_max)
        if system_size_max == 0.0:
            system_size_max = 30.1*149597870700
        return (-system_size_max, system_size_max)