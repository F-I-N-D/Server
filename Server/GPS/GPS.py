import time
from threading import Thread
from Server.Drone.HardwareDrone import HardwareDrone
import numpy as np
import cv2

DEFAULT_LIGHT_AREA = 1

class GPS(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__isRunnning = False
        self.drones = []

    def stop(self) -> None:
        self.__isRunnning = False

    def addDrone(self, drone: HardwareDrone) -> None:
        self.drones.append(drone)

    def run(self):
        self.__isRunnning = True

        cap = cv2.VideoCapture(2)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while True and self.__isRunnning:
            flag, imageFrame = cap.read()

            if(flag):
                imageFrame= cv2.add(imageFrame,np.array([-100.0]))

                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            
                red_lower = np.array([0, 100, 100], np.uint8)
                red_upper = np.array([19, 255, 255], np.uint8)
                red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

                green_lower = np.array([60, 100, 100], np.uint8)
                green_upper = np.array([109, 255, 255], np.uint8)
                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
            
                blue_lower = np.array([120, 100, 100], np.uint8)
                blue_upper = np.array([169, 255, 255], np.uint8)
                blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
                
                # Morphological Transform, Dilation
                # for each color and bitwise_and operator
                # between imageFrame and mask determines
                # to detect only that particular color
                kernal = np.ones((5, 5), "uint8")
                
                # For red color
                red_mask = cv2.dilate(red_mask, kernal)
                res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)

                # For green color
                green_mask = cv2.dilate(green_mask, kernal)
                res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)
                
                # For blue color
                blue_mask = cv2.dilate(blue_mask, kernal)
                res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask = blue_mask)
            
                colorList = []

                # Creating contour to track red color
                contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > DEFAULT_LIGHT_AREA):
                        x, y, w, h = cv2.boundingRect(contour)
                        colorList.append([x+int(w/2),y+int(h/2),'#FF0000'])
                        imageFrame = cv2.circle(imageFrame, (x+int(w/2),y+int(h/2)), radius=30, color=(0, 0, 255), thickness=10)     
            
                # Creating contour to track green color
                contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > DEFAULT_LIGHT_AREA):
                        x, y, w, h = cv2.boundingRect(contour)
                        colorList.append([x+int(w/2),y+int(h/2),'#00FF00'])
                        imageFrame = cv2.circle(imageFrame, (x+int(w/2),y+int(h/2)), radius=30, color=(0, 255, 0), thickness=10)
            
                # Creating contour to track blue color
                contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > DEFAULT_LIGHT_AREA):
                        x, y, w, h = cv2.boundingRect(contour)
                        colorList.append([x+int(w/2),y+int(h/2),'#0000FF'])
                        imageFrame = cv2.circle(imageFrame, (x+int(w/2),y+int(h/2)), radius=30, color=(255, 0, 0), thickness=10)

                #drones bepalen
                possibleDrones = []
                for idx, color in enumerate(colorList):
                    for nestedIdx, nestedColor in enumerate(colorList):
                        if(abs(colorList[idx][0] - colorList[nestedIdx][0]) <= 30 and abs(colorList[idx][1] - colorList[nestedIdx][1]) <= 30 and colorList[idx][2] != colorList[nestedIdx][2] and idx != nestedIdx):
                            possibleDrones.append([colorList[idx],colorList[nestedIdx]])

                for dronecolor in self.drones:
                    droneSeen = False
                    for drone in possibleDrones:
                        if(drone[0][2] == dronecolor.colorFront and drone[1][2] == dronecolor.colorBack):
                            dronex = int((drone[0][0] + drone[1][0]) / 2)
                            droney = int((drone[0][1] + drone[1][1]) / 2)
                            dronedir = np.arctan2(drone[1][1]-drone[0][1],drone[1][0]-drone[0][0]) * 180 / np.pi

                            dronecolor.locationX = dronex
                            dronecolor.locationY = droney
                            dronecolor.direction = dronedir
                            
                            droneSeen = True

                    if droneSeen or not drone.isFlying:
                        dronecolor.framesNotSeen = 0
                    else:
                        dronecolor.framesNotSeen += 1