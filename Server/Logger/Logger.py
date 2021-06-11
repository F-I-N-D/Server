from datetime import datetime
import os
from Server.Logger.Level import Level
from Server.Gui.Gui import Gui
from pathlib import Path

class Logger:
    # Start logger and create file to save logs in
    def __init__(self, level: Level = Level.Info):
        self.level = level
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.logFile = Path(f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}.log")
        self.gui = None

    # Log debug message
    def debug(self, message: str, droneId: str = None):
        if self.level <= Level.Debug:
            self.__writeLog("DEBUG", message, droneId)

    # Log info message
    def info(self, message: str, droneId: str = None):
        if self.level <= Level.Info:
            self.__writeLog("INFO", message, droneId)

    # Log warning message
    def warning(self, message: str, droneId: str = None):
        if self.level <= Level.Warning:
            self.__writeLog("WARNING", message, droneId)

    # Log error message
    def error(self, message: str, droneId: str = None):
        if self.level <= Level.Error:
            self.__writeLog("ERROR", message, droneId)

    # Log critical message
    def critical(self, message: str, droneId: str = None):
        if self.level <= Level.Critical:
            self.__writeLog("CRITICAL", message, droneId)

    # Add gui to the logger to display the logging on the gui
    def addGui(self, gui: Gui):
        self.gui = gui

    # Write log with color codes for the gui
    def __writeLog(self, level: str, message: str, droneId: str = None):
        currentDatetime = datetime.now().strftime("%H:%M:%S,%f")

        textStyling = ""
        if level == "CRITICAL":
            textStyling = "red bold"
        elif level == "ERROR":
            textStyling = "red"
        elif level == "WARNING":
            textStyling = "orange"
        elif level == "INFO":
            textStyling = "bright_green"
        elif level == "DEBUG":
            textStyling = "blue"

        if droneId:
            self.__writeToFile(f"[{currentDatetime}][{level}][{droneId}] {message}")
            self.__writeToGui(f"[[green]{currentDatetime}[/green]][[{textStyling}]{level}[/{textStyling}]][[blue]{droneId}[/blue]] {message}")
        else:
            self.__writeToFile(f"[{currentDatetime}][{level}] {message}")
            self.__writeToGui(f"[[green]{currentDatetime}[/green]][[{textStyling}]{level}[/{textStyling}]] {message}")

    # Log the log to the gui
    def __writeToGui(self, message: str):
        if self.gui:
            self.gui.logs.append(message)

    # Write the log to a file
    def __writeToFile(self, message: str):
        fil = open(self.logFile, "a")
        fil.write(f"{message}\n")
        fil.close()