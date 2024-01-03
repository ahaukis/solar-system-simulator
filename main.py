import sys
import gui
from PyQt5.QtWidgets import QApplication
from solar_system_scene import SolarSystemScene
import solar_system_file
from solar_system_error import *

def main():

    app = QApplication(sys.argv)

    try:
        with open('settings.csv', 'r') as file:
            settings_reader = solar_system_file.SolarSystemFile()
            try:
                system = settings_reader.read_settings_file(file)
            except SettingsFileError:
                msg = ErrorMessage("Error in reading settings file.")
            else:
                window = gui.GUI(system)
                sys.exit(app.exec_())
    except IOError:
        msg = ErrorMessage("Could not open settings file.")

if __name__ == '__main__':
    main()