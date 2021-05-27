from datetime import datetime
import os

class Logger:
    def __init__(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.logFile = f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}.log"

    def debug(self, message: str, droneId: str = None):
        self.__writeLog("DEBUG", message, droneId)

    def info(self, message: str, droneId: str = None):
        self.__writeLog("INFO", message, droneId)

    def warning(self, message: str, droneId: str = None):
        self.__writeLog("WARNING", message, droneId)

    def error(self, message: str, droneId: str = None):
        self.__writeLog("ERROR", message, droneId)

    def critical(self, message: str, droneId: str = None):
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