from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from planet_graphics_item import PlanetGraphicsItem

class SolarSystemScene(QGraphicsScene):

    def __init__(self, system):
        super().__init__()
        self.setBackgroundBrush(Qt.black)
        self.setSceneRect(0, 0, 500, 500)

        self.system = system
        self.size = system.get_size()[1]

        self.planet_items = []
        for planet in system.get_all_bodies():
            self.add_planet(planet)
    
    def get_size(self):
        return self.size

    def add_planet(self, planet):
        """
        Creates and adds a PlanetGraphicsItem to the scene.
        """
        planet_item = PlanetGraphicsItem(planet, self.size)
        self.planet_items.append(planet_item)
        self.addItem(planet_item)
    
    def update_items_to_planets(self):
        """
        Removes any PlanetGraphicsItems that are no longer in the system.
        """
        to_be_removed = []
        for planet_item in self.planet_items:
            if planet_item.get_planet() not in self.system.get_all_bodies():
                to_be_removed.append(planet_item)
        for planet_item in to_be_removed:
            self.removeItem(planet_item)
            self.planet_items.remove(planet_item)
    
    def update_planets(self):
        """
        Updates the position of all PlanetGraphicItems in the scene.
        """
        for planet_item in self.planet_items:
            planet_item.update_position()

class SolarSystemView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.setMinimumSize(500, 500)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.size = scene.get_size()

        self.setMouseTracking(True)
        self.mouse_pos = [0, 0]
        self.mouse_click = MouseClick()
    
    def get_mouse_pos(self):
        return self.mouse_pos
    
    def mouseReleaseEvent(self, event):
        """
        When a point in the SolarSystemView is clicked, it saves the clicked position (to the mouse_pos parameter) and emits a signal.
        """
        pos_x, pos_y = event.pos().x(), event.pos().y()
        real_x = 2*self.size*(pos_x/500) - self.size
        real_y = -2*self.size*(pos_y/500) + self.size
        self.mouse_pos = [real_x, real_y]
        self.mouse_click.signal.emit()


class MouseClick(QObject):
    signal = pyqtSignal()