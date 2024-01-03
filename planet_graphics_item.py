from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt5.QtCore import Qt, QPointF
from satellite import Satellite

class PlanetGraphicsItem(QGraphicsEllipseItem):

    def __init__(self, planet, system_size):

        self.planet = planet
        self.system_size = system_size

        # Set radius
        real_r = planet.get_radius()
        if isinstance(self.planet, Satellite):
            self.r = 5
        else:
            self.r = 5*(real_r/(0.00001*self.system_size))
        self.r *= 0.75*self.planet.get_position()[2]/self.system_size + 1   # Adjust size based on z-position.
        if self.r < 3:
            self.r = 3
        elif self.r > 8:
            self.r = 8
        
        # Determine position in scene
        real_x, real_y = planet.get_position()[0], planet.get_position()[1]
        self.x = 500*(self.system_size+real_x)/(2*self.system_size) - self.r
        self.y = 500 - 500*(self.system_size+real_y)/(2*self.system_size) - self.r

        super().__init__(self.x, self.y, 2*self.r, 2*self.r)

        # Set colour
        self.setBrush(QBrush(1))
        clr = self.planet.get_colour()
        self.setBrush(QColor(clr[0], clr[1], clr[2]))

        # Set velocity and acceleration vectors
        self.v, self.a = QGraphicsLineItem(), QGraphicsLineItem()
        self.v = self.set_vector_line(self.v, self.planet.get_velocity(), 0.01)
        self.a = self.set_vector_line(self.a, self.planet.get_acceleration(), 10000)
        self.set_vector_to_parent(self.v)
        self.set_vector_to_parent(self.a)
        self.v.setPen(QPen(Qt.blue, 1))
        self.a.setPen(QPen(Qt.red, 1))

        # Set arrow points to vectors
        self.v_point = ArrowPoint(self.v, 0, 3, 5, 0, 0, -3)
        self.a_point = ArrowPoint(self.a, 0, 3, 5, 0, 0, -3)
        self.v_point.setPen(QPen(Qt.blue, 1))
        self.a_point.setPen(QPen(Qt.red, 1))
        self.v_point.setBrush(QBrush(Qt.blue, 1))
        self.a_point.setBrush(QBrush(Qt.red, 1))

        self.v_point.update_triangle()
        self.a_point.update_triangle()
    
    def get_planet(self):
        return self.planet

    def update_position(self):
        """Moves the planet and its vectors according to their position in the system."""
        # Determine new position
        real_x, real_y = self.planet.get_position()[0], self.planet.get_position()[1]
        new_x = 500*(self.system_size+real_x)/(2*self.system_size) - self.r
        new_y = 500 - 500*(self.system_size+real_y)/(2*self.system_size) - self.r

        # Update vector arrows
        self.v = self.set_vector_line(self.v, self.planet.get_velocity(), 0.01)
        self.a = self.set_vector_line(self.a, self.planet.get_acceleration(), 10000)

        # Update vector arrow points
        self.v_point.update_triangle()
        self.a_point.update_triangle()

        # Move to new position
        self.setPos(new_x-self.x, new_y-self.y)
    
    def set_vector_to_parent(self, line_item):
        """Sets the line_item vector's parent to the current planet item."""
        line_item.setParentItem(self)
        # Sets vector starting point to the middle of the planet
        line_item.setPos(self.x+self.r, self.y+self.r)
        line_item.setFlag(QGraphicsLineItem.ItemStacksBehindParent)
    
    def set_vector_line(self, line_item, real_vector, scaling_factor):
        """
        Changes the length of the vector 'line_item' to match to real_vector.
        scaling_factor (float): scales real_vector so that it can be sensibly drawn on screen.
        """

        line_item.setLine(0, 0, scaling_factor*real_vector[0], -scaling_factor*real_vector[1])

        if line_item.line().length() < self.r+10:
            temp_line = line_item.line()
            temp_line.setLength(self.r+10)
            line_item.setLine(temp_line)
        elif line_item.line().length() > self.r+190:
            temp_line = line_item.line()
            temp_line.setLength(self.r+190)
            line_item.setLine(temp_line)

        return line_item

class ArrowPoint(QGraphicsPolygonItem):

    def __init__(self, parent_line, x1, y1, x2, y2, x3, y3):
        """
        Creates the arrow point defined by points 1, 2 and 3, that is attached to the parent line.
        """
        super().__init__()
        triangle = QPolygonF()
        triangle.append(QPointF(x1, y1))
        triangle.append(QPointF(x2, y2))
        triangle.append(QPointF(x3, y3))
        self.setPolygon(triangle)

        self.parent_line = parent_line

        self.setParentItem(self.parent_line)
        self.setPos(self.parent_line.line().dx(), self.parent_line.line().dy())
    
    def update_triangle(self):
        # Moves and rotates the arrow point according to the current position of the parent line.
        self.setRotation(-self.parent_line.line().angle())
        self.setPos(self.parent_line.line().dx(), self.parent_line.line().dy())