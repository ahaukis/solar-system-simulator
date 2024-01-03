from celestial_body import CelestialBody
from satellite import Satellite
from physics import Physics, DIMENSION

class SolarSystem:

    def __init__(self):
        self.celestial_bodies = []
        self.solar_system_size = (0,0)      # (min, max) coordinates

        # Current time, time step of the simulation and the maximum duration of the simulation, all in seconds.
        self.t = 0
        self.dt = 0
        self.lifespan = 0

        self.satellites_inside_system = True
        self.impact = False
        self.physics = Physics()

        self.saved_bodies = []
        self.saved_state = []
    
    def save_state(self):
        """
        Saves the current bodies in the system and their physical parameters.
        """
        for body in self.celestial_bodies:
            self.saved_bodies.append(body)
            pos, vel, acc = body.get_position(), body.get_velocity(), body.get_acceleration()
            self.saved_state.append([pos, vel, acc])
    
    def return_to_saved_state(self):
        """
        Compares the current system to the saved state, removes any bodies that have since been added and sets the remaining bodies back to their saved states (position, speed etc.).
        """
        to_be_removed = []
        for body in self.celestial_bodies:
            if body not in self.saved_bodies:
                to_be_removed.append(body)
        for body in to_be_removed:
            self.celestial_bodies.remove(body)
        for i in range(len(self.celestial_bodies)):
            body = self.celestial_bodies[i]
            body.update_position(self.saved_state[i][0])
            body.update_velocity(self.saved_state[i][1])
            body.update_acceleration(self.saved_state[i][2])
        
        # Resets possible simulation-stopping events.
        self.set_satellite_status(True)
        self.impact = False
    
    def set_satellite_status(self, boolean):
        self.satellites_inside_system = boolean
    
    def get_all_bodies(self):
        return self.celestial_bodies

    def get_body(self, name):
        """
        Returns the body with name "name" (string), else returns False.
        """
        for body in self.celestial_bodies:
            if body.get_name() == name:
                return body
        return False
    
    def get_size(self):
        return self.solar_system_size
    
    def get_time(self):
        return self.t
    
    def get_lifespan(self):
        return self.lifespan
    
    def impact_status(self):
        return self.impact

    def satellites_status(self):
        return self.satellites_inside_system

    def next_time_step(self):
        """Moves time forward by 1 time step and calls the Runge-Kutta-4-method to update the situation of the system."""
        self.celestial_bodies = self.physics.rk4(self.celestial_bodies, self.dt)
        self.t += self.dt
    
    def check_impact(self):
        """
        Checks if any objects in the solar system have collided.
        """
        for i in range(len(self.celestial_bodies)):
            for j in range(len(self.celestial_bodies)):
                if i < j:
                    body1 = self.celestial_bodies[i]
                    body2 = self.celestial_bodies[j]
                    if self.physics.abs_distance(body1.get_position(), body2.get_position()) <= body1.get_radius() + body2.get_radius():
                        self.impact = True

    def check_satellites(self):
        """
        Checks if a satellite has flown out of the system.
        """
        for body in self.celestial_bodies:
            if isinstance(body, Satellite):
                for i in range(DIMENSION):
                    if body.get_position()[i] < self.solar_system_size[0] or body.get_position()[i] > self.solar_system_size[1]:
                        self.satellites_inside_system = False

    def add_to_system(self, body):
        """
        Adds a body to the solar system.
        """
        self.celestial_bodies.append(body)
    
    def remove_from_system(self, body):
        """
        Removes a body from the solar system.
        """
        self.celestial_bodies.remove(body)
    
    def set_size(self, size):
        """
        Sets the size of the solar system.
        """
        self.solar_system_size = size
    
    def set_time_step(self, time_step):
        """
        Set the time step of the simulation (in seconds).
        """
        self.dt = time_step
    
    def set_lifespan(self, lifespan):
        """Set how long the simulation will last at most (in seconds)."""
        self.lifespan = lifespan

    def set_time(self, time):
        """
        Set the current time of the simulation (in seconds).
        """
        self.t = time