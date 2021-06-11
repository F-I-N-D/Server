from datetime import datetime
import os
from Server.Logger.Level import Level
# from Server.Gui.Gui import Gui
from pathlib import Path

class Logger:
    def __init__(self, level: Level = Level.Info):
        self.level = level
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.logFile = Path(f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}.log")
        self.gui = None

    def debug(self, message: str, droneId: str = None):
        if self.level <= Level.Debug:
            self.__writeLog("DEBUG", message, droneId)

    def info(self, message: str, droneId: str = None):
        if self.level <= Level.Info:
            self.__writeLog("INFO", message, droneId)

    def warning(self, message: str, droneId: str = None):
        if self.level <= Level.Warning:
            self.__writeLog("WARNING", message, droneId)

    def error(self, message: str, droneId: str = None):
        if self.level <= Level.Error:
            self.__writeLog("ERROR", message, droneId)

    def critical(self, message: str, droneId: str = None):
        if self.level <= Level.Critical:
            self.__writeLog("CRITICAL", message, droneId)

    def addGui(self, gui):
        self.gui = gui

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

    def __writeToGui(self, message: str):
        if self.gui:
            self.gui.logs.append(message)

    def __writeToFile(self, message: str):
        fil = open(self.logFile, "a")
        fil.write(f"{message}\n")
        fil.close()