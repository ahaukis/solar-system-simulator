import physics

class CelestialBody:
    """
    Class to represent all celestial bodies in the solar system to be simulated.
    """

    def __init__(self, name, mass, radius, position, velocity, colour):

        self.name = name
        self.m = mass
        self.r = radius
        self.x = position
        self.v = velocity
        self.a = [0 for i in range(physics.DIMENSION)]              # acceleration
        self.colour = colour

    def get_name(self):
        return self.name

    def get_position(self):
        return self.x
    
    def get_mass(self):
        return self.m
    
    def get_radius(self):
        return self.r

    def get_position(self):
        return self.x

    def get_velocity(self):
        return self.v
    
    def get_acceleration(self):
        return self.a
    
    def get_colour(self):
        return self.colour
    
    def update_position(self, position):
        self.x = position
    
    def update_velocity(self, velocity):
        self.v = velocity
    
    def update_acceleration(self, acceleration):
        self.a = acceleration