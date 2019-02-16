#!/usr/bin/python
import wpilib
import wpilib.buttons
#import zmq
#import numpy as np
class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005 #this is 5 milliseconds
    def robotInit(self):
        self.talon0 = wpilib.Talon(1) #CAN starts on #0
        self.talon1 = wpilib.Talon(2)
        self.talon2 = wpilib.Talon(3) #end of left side
        self.talon3 = wpilib.Talon(4)
        self.talon4 = wpilib.Talon(5)
        self.talon5 = wpilib.Talon(6) #end of right side
        self.xbox = wpilib.XboxController(0) #Init joystick on port #0 TOP RIGHT on driverstation!
        self.left = wpilib.SpeedControllerGroup(self.talon1, self.talon2, self.talon3)
        self.right = wpilib.SpeedControllerGroup(self.talon4, self.talon5, self.talon6)
        self.myRobot = DifferentialDrive(self.left, self.right) #set up diff drive using all 6 talons
        self.myRobot.setExpiration(0.1) #safety expiration of 10ms / 5ms without signal before stopping
    def autonomousInit(self):
        self.myRobot.setSafetyEnabled(True) #since we are driving the robot in auto
    def autonomousPeriodic(self):
        self.myRobot.tankDrive(self.xbox.getY(0), self.xbox.getY(1)) #possibly add throttle curve
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
        #context = zmq.Context()
        #angle_socket = context.socket(zmq.SUB)
        #angle_socket.bind('tcp://*:5556')
        #angle_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    def teleopPeriodic(self):
        #angle=angle.recv_string()
        #navigate to angle, continue
        self.myRobot.tankDrive(self.xbox.getY(0), self.xbox.getY(1)) #possibly add throttle curve
        #self.myRobot.tankDrive(self.leftStick.getY()**2 * -1, self.rightStick.getY()**2 * -1) #for two joystick control
if __name__ == "__main__":
    wpilib.run(MyRobot)