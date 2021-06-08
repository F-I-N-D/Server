from datetime import datetime
import os
from Server.Logger.Level import Level

class Logger:
    def __init__(self, level: Level = Level.Info):
        self.level = level
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.logFile = f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}.log"

    def debug(self, message: str, droneId: str = None):
        if self.level >= Level.Debug:
            self.__writeLog("DEBUG", message, droneId)

    def info(self, message: str, droneId: str = None):
        if self.level >= Level.Info:
            self.__writeLog("INFO", message, droneId)

    def warning(self, message: str, droneId: str = None):
        if self.level >= Level.Warning:
            self.__writeLog("WARNING", message, droneId)

    def error(self, message: str, droneId: str = None):
        if self.level >= Level.Err:
            self.__writeLog("ERROR", message, droneId)

    def critical(self, message: str, droneId: str = None):
        if self.level >= Level.Critical:
            self.__writeLog("CRITICAL", message, droneId)

    def __writeLog(self, level: str, message: str, droneId: str = None):
        currentDatetime = datetime.now().strftime("%H:%M:%S,%f")
        if droneId:
            self.__writeToFile(f"[{currentDatetime}][{level}][{droneId}] {message}")
        else:
            self.__writeToFile(f"[{currentDatetime}][{level}] {message}")

    def __writeToFile(self, message: str):
        fil = open(self.logFile, "a")
        fil.write(f"{message}\n")
        fil.close()