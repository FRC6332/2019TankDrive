#!/usr/bin/python
import wpilib
import wpilib.buttons
#import zmq
#import numpy as np
class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005 #this is 5 milliseconds
    def robotInit(self):
        self.talon0 = wpilib.Talon(0) #CAN starts on #0
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
        wpilib.CameraServer.launch('vision.py:main') #possibly put this in autonomousInit
    def autonomousInit(self):
        self.myRobot.setSafetyEnabled(True) #since we are driving the robot in auto
    def autonomousPeriodic(self):
        z=self.stick.getZ()
        if self.button0.get() == 0:
            z=0
        self.myRobot.tankDrive(-(self.stick.getY() * abs(self.stick.getY())) + z*abs(z), -(self.stick.getY() * abs(self.stick.getY())) - z*abs(z)) #simple x^2 throttle curve
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
        #context = zmq.Context()
        #angle_socket = context.socket(zmq.SUB)
        #angle_socket.bind('tcp://*:5556')
        #angle_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    def teleopPeriodic(self):
        #angle=angle.recv_string()
        #navigate to angle, continue
        z=self.stick.getZ()
        if self.button0.get() == 0:
            z = 0
         self.myRobot.tankDrive(-(self.stick.getY() * abs(self.stick.getY())) + z*abs(z), -(self.stick.getY() * abs(self.stick.getY())) - z*abs(z)) #simple x^2 throttle curve
        #self.myRobot.tankDrive(self.leftStick.getY()**2 * -1, self.rightStick.getY()**2 * -1) #for two joystick control
if __name__ == "__main__":
    wpilib.run(MyRobot)