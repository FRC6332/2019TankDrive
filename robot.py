#!/usr/bin/python
import wpilib
import wpilib.buttons

import cv2
import zmq
import base64
import numpy as np


class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005 #this is 5 milliseconds, or 200 fps for sandstream (though it'll probably be capped much lower)
    def robotInit(self):
        self.talon0 = wpilib.Talon(0) #CAN starts on #1 or 0? Don't make the same mistake as last year
        self.talon1 = wpilib.Talon(1)
        self.talon2 = wpilib.Talon(2) #end of left side
        self.talon3 = wpilib.Talon(3)
        self.talon4 = wpilib.Talon(4)
        self.talon5 = wpilib.Talon(5) #end of right side
        self.stick = wpilib.Joystick(0) #Init joystick on port #0 TOP RIGHT on driverstation!
        self.left = wpilib.SpeedControllerGroup(self.talon0, self.talon1, self.talon2)
        self.right = wpilib.SpeedControllerGroup(self.talon3, self.talon4, self.talon5)
        self.myRobot = DifferentialDrive(self.left, self.right) #set up diff drive using all 6 talons
        self.myRobot.setExpiration(0.1) #safety expiration of 10ms / 5ms without signal before stopping
    def autonomousInit(self):
        #set up camera server
        cs=CameraServer.getInstance()
        cs.enableLogging()
        outputStream = cs.putVideo("Sandstream", 320, 240)
        #set up zmq and init an empty image frame
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://*:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    def autonomousPeriodic(self):
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        #source = cv2.imdecode(npimg, 1)
        outputStream.putFrame(img)
        z=self.stick.getZ()
        if self.button0.get() == 0:
            z=0
        self.myRobot.tankDrive(-(self.stick.getY() * abs(self.stick.getY())) + z*abs(z), -(self.stick.getY() * abs(self.stick.getY())) - z*abs(z)) #simple x^2 throttle curve
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
    def teleopPeriodic(self):
        z=self.stick.getZ()
        if self.button0.get() == 0:
            z = 0
         self.myRobot.tankDrive(-(self.stick.getY() * abs(self.stick.getY())) + z*abs(z), -(self.stick.getY() * abs(self.stick.getY())) - z*abs(z)) #simple x^2 throttle curve
        #self.myRobot.tankDrive(self.leftStick.getY()**2 * -1, self.rightStick.getY()**2 * -1) #for two joystick control
if __name__ == "__main__":
wpilib.run(MyRobot)
