from PyQt5.QtWidgets import QMessageBox

class SolarSystemError(Exception):
    pass

class SettingsFileError(SolarSystemError):
    def __init__(self, message):
        self.message = message

class ErrorMessage(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setText(message)
        self.setWindowTitle("Error")
        self.exec()