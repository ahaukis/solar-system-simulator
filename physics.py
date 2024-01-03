from math import sqrt

DIMENSION = 3
GRAV_CONSTANT = 6.67408e-11 # m^3/(kg*s)
LIGHTSPEED = 299792458 # m/s

class Physics:

    def rk4(self, celestial_bodies, h):
        """
        Calculates and updates the acceleration, velocity and position of all objects in celestial_bodies.
        The velocity is calculated using the 4th order Runge-Kutta method, while the positon is updated using Euler's method.
        Returns the updated list.

        celestial_bodies: list of all objects
        h: time step
        """
        # Save the initial values of all objects
        a_1 = [celestial_bodies[i].get_acceleration() for i in range(len(celestial_bodies))]
        a_2 = 0
        a_3 = 0
        a_4 = 0

        v_0 = [celestial_bodies[i].get_velocity() for i in range(len(celestial_bodies))]
        v_1 = 0
        v_2 = 0
        v_3 = 0

        pos_0 = [celestial_bodies[i].get_position() for i in range(len(celestial_bodies))]
        pos_1 = 0
        pos_2 = 0
        pos_3 = 0

        final_v = [[0 for j in range(DIMENSION)] for i in range(len(celestial_bodies))]
        final_pos = [[0 for j in range(DIMENSION)] for i in range(len(celestial_bodies))]
        final_a = [[0 for j in range(DIMENSION)] for i in range(len(celestial_bodies))]

        # Iterate over each body to find final acceleration, velocity and position.
        for x in range(len(celestial_bodies)):

            v_1 = [(v_0[x][i] + a_1[x][i]*(h/2)) for i in range(DIMENSION)]
            pos_1 = [(pos_0[x][i] + v_0[x][i]*(h/2)) for i in range(DIMENSION)]
            celestial_bodies[x].update_position(pos_1)
        
            a_2 = self.acceleration(self.net_force(celestial_bodies[x], celestial_bodies), celestial_bodies[x].get_mass())

            v_2 = [(v_0[x][i] + a_2[i]*(h/2)) for i in range(DIMENSION)]
            pos_2 = [(pos_0[x][i] + v_1[i]*(h/2)) for i in range(DIMENSION)]
            celestial_bodies[x].update_position(pos_2)

            a_3 = self.acceleration(self.net_force(celestial_bodies[x], celestial_bodies), celestial_bodies[x].get_mass())
    
            v_3 = [(v_0[x][i] + a_3[i]*h) for i in range(DIMENSION)]
            pos_3 = [(pos_0[x][i] + v_2[i]*h) for i in range(DIMENSION)]
            celestial_bodies[x].update_position(pos_3)

            a_4 = self.acceleration(self.net_force(celestial_bodies[x], celestial_bodies), celestial_bodies[x].get_mass())

            final_v[x] = [(v_0[x][i] + (h/6)*(a_1[x][i] + 2*(a_2[i] + a_3[i]) + a_4[i])) for i in range(DIMENSION)]
            final_pos[x] = [(pos_0[x][i] + h*v_0[x][i]) for i in range(DIMENSION)]
            final_a[x] = self.acceleration(self.net_force(celestial_bodies[x], celestial_bodies), celestial_bodies[x].get_mass())

            # Set the body back to starting position
            celestial_bodies[x].update_position(pos_0[x])

        # Update all bodies with their new values
        for x in range(len(celestial_bodies)):
            celestial_bodies[x].update_acceleration(final_a[x])
            celestial_bodies[x].update_velocity(final_v[x])
            celestial_bodies[x].update_position(final_pos[x])
        
        # Return the updated list
        return celestial_bodies

    def gravitational_force(self, mass1, mass2, r):
        """
        Calculates the gravitational force between two bodies as a list of components.

        mass1, mass2: masses of the two bodies
        r: distance between the bodies in vector components
        """
        grav_force = [0 for i in range(DIMENSION)]
        total_r = self.vector_length(r)
        total_grav_force = GRAV_CONSTANT*((mass1*mass2)/total_r**2)

        for i in range(DIMENSION):
            grav_force[i] = total_grav_force*(r[i]/total_r)

        return grav_force
    
    def net_force(self, body, celestial_bodies):
        """
        Calculates the net force of gravity affecting body in question.
        
        body: target body
        celestial_bodies: list of all bodies in the system (including target body)
        """
        net_force = [0 for i in range(DIMENSION)]   # N
        others = celestial_bodies[:]
        others.remove(body)
        for x in others:
            grav_force = self.gravitational_force(body.get_mass(), x.get_mass(), self.displacement(body.get_position(), x.get_position()))
            for i in range(DIMENSION):
                net_force[i] += grav_force[i]
        return net_force
    
    def displacement(self, x1, x2):
        """Calculates displacement between vector x1 and vector x2."""
        dist_components = [(x2[i] - x1[i]) for i in range(DIMENSION)]
        return dist_components
    
    def abs_distance(self, x1, x2):
        """Calculates absolute distance between positions 1 and 2."""
        return self.vector_length(self.displacement(x1, x2))
    
    def speed(self, body):
        """Calculates speed of body."""
        return self.vector_length(body.get_velocity())
    
    def acceleration(self, net_force, mass):
        """Calculates acceleration"""
        return [net_force[i]/mass for i in range(DIMENSION)]
    
    def vector_length(self, vector):
        """Takes list of vector components and calculates the length of the vector in question."""
        component_list = vector[:]
        for i in range(len(component_list)):
            component_list[i] **= 2
        return sqrt(sum(component_list))