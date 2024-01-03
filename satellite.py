from celestial_body import *

class Satellite(CelestialBody):

    def __init__(self, mass, position, velocity):
        name = None
        radius = 0
        colour = [255, 255, 255]        # white
        super().__init__(name, mass, radius, position, velocity, colour)