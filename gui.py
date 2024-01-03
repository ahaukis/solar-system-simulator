from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from solar_system_scene import *
from solar_system_error import ErrorMessage
import physics
from satellite import Satellite
from time import sleep

class GUI(QtWidgets.QMainWindow):

    def __init__(self, system):
        super().__init__()
        self.system = system
        self.init_ui()
        self.reset_gui()

        # Simulation is not currently running
        self.running = False

    def init_ui(self):

        self.setWindowTitle('Solar System Simulator')
        self.setGeometry(0, 0, 750, 550)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.resize(250, 550)

        grid = QtWidgets.QGridLayout()

        # Create the 'add satellites' button
        self.satellite_button = self.init_add_satellite(grid)
        self.satellite_button.clicked.connect(self.add_satellite)

        # Create the simulatio parameters sliders
        self.init_sim_parameters(grid)

        # Create the button to start, stop simulation
        self.run_button = QtWidgets.QPushButton()
        grid.addWidget(self.run_button, 11, 0, 1, 3)

        self.scene = SolarSystemScene(self.system)
        self.view = SolarSystemView(self.scene)

        self.view.mouse_click.signal.connect(self.show_coordinates) # Clicking on the view will choose the current coordinates for the satellite text fields

        # Create status bar to show information about the simulation
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)

        grid.addWidget(self.view, 0, 4, 12, 1)

        self.central_widget.setLayout(grid)

        self.show()
        self.view.show()
    
    def show_coordinates(self):
        """
        Gets the (real) coordinates of the mouse on the view, and sets them to the corresponding text fields.
        """
        pos = self.view.get_mouse_pos()
        self.posX.setText(str(pos[0]))
        self.posY.setText(str(pos[1]))
    
    def init_add_satellite(self, grid):
        """
        Creates the text fields that are used to add a new satellite to the system.
        Returns the button used to accept the satellite.
        """
        self.satellite_title = QtWidgets.QLabel('ADD SATELLITES:')

        self.mass, self.speed, self.pos = QtWidgets.QLabel('m (kg)'),  QtWidgets.QLabel('v (m/s)'),  QtWidgets.QLabel('position (m)')
        self.mass_edit= QtWidgets.QLineEdit()

        self.speedX, self.speedY, self.speedZ = QtWidgets.QLineEdit(), QtWidgets.QLineEdit(), QtWidgets.QLineEdit()
        self.speedX.setPlaceholderText('X')
        self.speedY.setPlaceholderText('Y')
        self.speedZ.setPlaceholderText('Z')

        self.posX, self.posY, self.posZ = QtWidgets.QLineEdit(), QtWidgets.QLineEdit(), QtWidgets.QLineEdit()
        self.posX.setPlaceholderText('X')
        self.posY.setPlaceholderText('Y')
        self.posZ.setPlaceholderText('Z')

        # List to hold all text fields so they can be easily cleared later
        self.line_edits = [self.mass_edit, self.speedX, self.speedY, self.speedZ, self.posX, self.posY, self.posZ]

        self.add_satellite_button = QtWidgets.QPushButton('Add')

        # Pressing enter in the last text fields acts like clicking the 'add' button
        self.posZ.returnPressed.connect(self.add_satellite)

        # Add text fields and titles to the layout
        grid.addWidget(self.satellite_title, 0, 0, 1, 3)
        grid.addWidget(self.mass_edit, 2, 0)
        grid.addWidget(self.speedX, 1, 1)
        grid.addWidget(self.speedY, 2, 1)
        grid.addWidget(self.speedZ, 3, 1)
        grid.addWidget(self.posX, 1, 2)
        grid.addWidget(self.posY, 2, 2)
        grid.addWidget(self.posZ, 3, 2)
        grid.addWidget(self.mass, 4, 0)
        grid.addWidget(self.speed, 4, 1)
        grid.addWidget(self.pos, 4, 2, 1, 1)
        grid.addWidget(self.add_satellite_button, 5, 0, 1, 3)

        return self.add_satellite_button
    
    def init_sim_parameters(self, grid):
        """
        Create the sliders to choose the simulation max duration and simulation time step.
        """
        self.parameters_title = QtWidgets.QLabel('SIMULATION PARAMETERS:')

        # Create sim length slider
        self.t_title = QtWidgets.QLabel('Duration')
        self.t_slider = QtWidgets.QSlider(Qt.Horizontal, self)
        # Slider range in months
        self.t_slider.setMinimum(1)
        self.t_slider.setMaximum(240)
        self.t_slider.setValue(36)
        self.t_label = QtWidgets.QLabel("{:5.2f} years".format(self.t_slider.value()/12))
        self.t_slider.valueChanged.connect(lambda: self.t_label.setText("{:5.2f} years".format(self.t_slider.value()/12)))

        # Sim time step slider
        self.dt_title = QtWidgets.QLabel('Time step')
        self.dt_slider = QtWidgets.QSlider(Qt.Horizontal, self)
        # Time step range in days
        self.dt_slider.setMinimum(1)
        self.dt_slider.setMaximum(7)
        self.dt_label = QtWidgets.QLabel("{:5d} days".format(self.dt_slider.value()))
        self.dt_slider.valueChanged.connect(lambda: self.dt_label.setText("{:5d} days".format(self.dt_slider.value())))

        grid.addWidget(self.parameters_title, 6, 0, 1, 3)

        grid.addWidget(self.t_title, 7, 0, 1, 3)
        grid.addWidget(self.t_slider, 8, 0, 1, 2)
        grid.addWidget(self.t_label, 8, 2)

        grid.addWidget(self.dt_title, 9, 0, 1, 3)
        grid.addWidget(self.dt_slider, 10, 0, 1, 2)
        grid.addWidget(self.dt_label, 10, 2)
    
    def add_satellite(self):
        """
        Adds satellite to solar system.
        """
        try:
            mass = float(self.mass_edit.text())
            velocity = [float(self.speedX.text()), float(self.speedY.text()), float(self.speedZ.text())]
            position = [float(self.posX.text()), float(self.posY.text()), float(self.posZ.text())]
        except ValueError:
            msg = ErrorMessage("Invalid values, try again.")
            for text_field in self.line_edits:
                text_field.clear()  # Clears text fields in case of bad input
        else:
            if mass <= 0:
                msg = ErrorMessage("Mass must be positive.")
                self.line_edits[0].clear()  # Clear mass text field
            else:
                satellite = Satellite(mass, position, velocity)
                if physics.Physics().speed(satellite) >= physics.LIGHTSPEED:
                    msg = ErrorMessage("The speed of a satellite cannot be more than the speed of light.")
                    for i in range(1, 4):
                        self.line_edits[i].clear()  # Clear the speed text fields
                else:
                    self.system.add_to_system(satellite)

                    # Check that the satellites position is within the system limits.
                    self.system.check_satellites()
                    if self.system.satellites_status() == False:
                        self.system.remove_from_system(satellite)
                        self.system.set_satellite_status(True)
                        msg = ErrorMessage("Satellite is too far away.")
                        for i in range(4, 7):
                            self.line_edits[i].clear()  # Clear the position text fields
                    else:
                        # Calculate the initial acceleration for the satellite
                        satellite.update_acceleration(physics.Physics().acceleration(physics.Physics().net_force(satellite, self.system.get_all_bodies()), satellite.get_mass()))
                        # Add satellite to system
                        self.scene.add_planet(satellite)
                        for text_field in self.line_edits:
                            text_field.clear()  # Clear all text fields
    
    def run_simulation(self):
        self.simulation_running_changed()

        # Disables all interactions to add satellites or change simulation parameters
        for text_field in self.line_edits:
            text_field.clear()
            text_field.setEnabled(False)
        self.add_satellite_button.setEnabled(False)
        self.t_slider.setEnabled(False)
        self.dt_slider.setEnabled(False)
        self.view.setMouseTracking(False)
        self.view.setToolTip('')

        self.run_button.setText("Quit simulation")
        self.run_button.disconnect()
        self.run_button.clicked.connect(self.simulation_running_changed)

        sim_length = self.t_slider.value()*30*24*60*60      # seconds
        sim_time_step = self.dt_slider.value()*24*60*60     # seconds
        self.system.set_lifespan(sim_length)
        self.system.set_time_step(sim_time_step)

        while self.running and self.system.get_time() < self.system.get_lifespan() and self.system.impact_status() == False and self.system.satellites_status() == True:
            self.animate_system()
            self.status_bar.showMessage('Time elapsed: {:3.2f} years'.format(self.system.get_time()/315.36e5))
            QtWidgets.QApplication.processEvents()
            sleep(0.01)
        
        self.simulation_over()
    
    def animate_system(self):
        # Call the next time step to be calculated
        self.system.next_time_step()
        # Check that objecst haven't collided and that satellites haven't flown away
        self.system.check_impact()
        self.system.check_satellites()
        # Update the scene to match the current system
        self.scene.update_planets()
    
    def simulation_running_changed(self):
        """Changes the simulation running state from True -> False and False -> True."""
        if self.running:
            self.running = False
        else:
            self.running = True

    def simulation_over(self):
        # Set the run button to reset the simulation
        self.run_button.setText('Reset')
        self.run_button.disconnect()
        self.run_button.clicked.connect(self.reset_gui)

        # Display the reason for the simulation ending
        if self.system.impact_status() == True:
            self.status_bar.showMessage('Simulation ended by collision')
        elif self.system.satellites_status() == False:
            self.status_bar.showMessage('Satellite flew away from system')
        else:
            self.status_bar.showMessage('Simulation over')
        
        # Changes the running value to false if it isn't that already
        if self.running:
            self.simulation_running_changed()
    
    def reset_gui(self):
        """
        Sets all GUI interactions (add satellite, choose time step etc.) available
        """
        # Enables the simulation settings
        for text_field in self.line_edits:
            text_field.setEnabled(True)
        self.add_satellite_button.setEnabled(True)
        self.t_slider.setEnabled(True)
        self.dt_slider.setEnabled(True)

        # Sets the run button to run simulation again
        self.run_button.setText('Run simulation')
        self.run_button.disconnect()
        self.run_button.clicked.connect(self.run_simulation)

        # Sets the view tooltip and click on
        self.view.setToolTip('Click to choose coordinates')
        self.view.setMouseTracking(True)

        # Resets the system and scene
        self.reset_system()

        self.status_bar.showMessage('Time elapsed: {:3.2f} years'.format(self.system.get_time()/315.36e5))
    
    def reset_system(self):
        """Sets the simulation back to its settings file state."""

        self.system.set_time(0)

        # Set the system back to the settings file state
        self.system.return_to_saved_state()
        # Remove any items from the scene that no longer match the system
        self.scene.update_items_to_planets()

        # Update the planets' graphic positions to match the current system
        self.scene.update_planets()