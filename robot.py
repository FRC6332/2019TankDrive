#!/usr/bin/python
import wpilib
import wpilib.buttons
from robotpy_ext.autonomous import AutonomousModeSelector
class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005
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
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
    def teleopPeriodic(self):
        self.myRobot.tankDrive(self.stick.getX()**2 * -1, self.stick.getY()**2 * -1) #simple x^2 throttle curve
        #self.myRobot.tankDrive(self.leftStick.getY()**2 * -1, self.rightStick.getY()**2 * -1) #for two joystick control
if __name__ == "__main__":
wpilib.run(MyRobot)
