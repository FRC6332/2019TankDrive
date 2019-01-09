#!/usr/bin/python
import wpilib
import wpilib.drive
import wpilib.buttons
import ctre
import cv2
import zmq #Figure out manual installation (SSH to RoboRio)
import base64
import numpy as np
from cscore import CameraServer
from robotpy_ext.autonomous import AutonomousModeSelector
class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005 #this is 5 milliseconds, or 200 fps
    def robotInit(self):
        self.talon0 = ctre.WPI_TalonSRX(0) #CAN starts on #1 or 0? Don't make the same mistake as last year
        self.talon1 = ctre.WPI_TalonSRX(1)#end of left side
        self.talon2 = ctre.WPI_TalonSRX(2) 
        self.talon3 = ctre.WPI_TalonSRX(3)# end of right side
        self.left_encoder = wpilib.Encoder(0, 1)
        self.right_encoder = wpilib.Encoder(2, 3)
        #self.talon4 = wpilib.Talon(4)
        #self.talon5 = wpilib.Talon(5) #end of right side
        self.stick = wpilib.Joystick(0) #Init joystick on port #0 TOP RIGHT on driverstation!
        self.button0 =wpilib.buttons.JoystickButton(self.stick, 2)
        self.button10 = wpilib.buttons.JoystickButton(self.stick, 10)
        self.left = wpilib.SpeedControllerGroup(self.talon0, self.talon1)#, self.talon2)
        self.right = wpilib.SpeedControllerGroup(self.talon2, self.talon3)#, self.talon5)
        self.myRobot = wpilib.drive.DifferentialDrive(self.left, self.right) #set up diff drive using all 6 talons
        self.myRobot.setExpiration(0.1) #safety expiration of 10ms / 5ms without signal before stopping
    def autonomousInit(self):
        cs=CameraServer.getInstance()
        cs.enableLogging()
        outputStream = cs.putVideo("Sandstream", 320, 240)
        img = np.zeros(shape=(240, 320, 3), dtype=np.uint8) #preallocate (may need to remove this)
        context=zmq.Context()
        bindsock = context.socket(smq.SUB)
        bindsock.bind('tcp://*:5555')
        bindsock.setsockopt_string(zmq.SUBSCRIBE, unicode(''))
    def autonomousPeriodic(self):
        frame = bindsock.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8) #should be compatible with putFrame
        outputStream.putFrame(img)
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
    def teleopPeriodic(self):
        #Using the Z axis for turning:
        #The Z axis of the joystick, like Y and X axis it varies from -1 to 1, -1 being all the way to the left and 1 being all the way to the right.
        #When the robot is still and the Z axis is at -1, the right side should be driving in reverse at full power and the left side should be driving forward at full power. (Turning in place)
        #Pseudo code: TankDrive(RightSide - zAxis, LeftSide + zAxis)
        #Including the Y axis:
        #Let's say the Y axis is at 1 (Full forward) and the Z axis is at -1. This should make the left side stop, and the right side go at full power.
        #Pseudo code: TankDrive(yAxis + zAxis, yAxis - zAxis)
        #To do this using robotpy we can say: 
        #self.myRobot.tankDrive(self.stick.getY() + self.stick.getZ(), self.stick.getY() - self.stick.getZ())
        #Since out drivetrains are inverted for whatever reason we actually need:
        #self.myRobot.tankDrive(-self.stick.getY() - self.stick.getZ(), -self.stick.getY() + self.stick.getZ())
        #Let's add a simple x^2 throttle curve. We can't simply just say yAxis**2 because that would be positive, no matter the value. 
        #Instead, I used yAxis * abs(yAxis), which is the yAxis times the absolute value of the yAxis. This way we can get our negitave values.
        #Adding this all up we have:
        z=self.stick.getZ()
        if self.button0.get() == 0:
           z = 0
        if self.button10.get() == 1:
            self.left_encoder.reset()
            self.right_encoder.reset()
        self.myRobot.tankDrive(-(self.stick.getY() * abs(self.stick.getY())) + z*abs(z), -(self.stick.getY() * abs(self.stick.getY())) - z*abs(z)) #simple x^2 throttle curve
        print(-self.left_encoder.getDistance(), self.right_encoder.getDistance())
        #self.myRobot.tankDrive(self.stick0.getY(),self.stick1.getY())
        #self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1) #for two joystick control
if __name__ == "__main__":
wpilib.run(MyRobot)