#!/usr/bin/python
import wpilib
import wpilib.drive
import ctre
class MyRobot(wpilib.IterativeRobot):
    kUpdatePeriod = 0.005
    def robotInit(self):
        self.talon0 = ctre.WPI_TalonSRX(0) #CAN starts on #1 or 0? Don't make the same mistake as last year
        self.talon1 = ctre.WPI_TalonSRX(1)#end of left side
        self.talon2 = ctre.WPI_TalonSRX(2)
        self.talon3 = ctre.WPI_TalonSRX(3)# end of right side
        #self.talon4 = wpilib.Talon(4)
       	#self.talon5 = wpilib.Talon(5) #end of right side
        self.stick = wpilib.Joystick(0) #Init joystick on port #0 TOP RIGHT on driverstation!

        self.left = wpilib.SpeedControllerGroup(self.talon0, self.talon1)#, self.talon2)
        self.right = wpilib.SpeedControllerGroup(self.talon2, self.talon3)#, self.talon5)

        self.myRobot = wpilib.drive.DifferentialDrive(self.left, self.right) #set up diff drive using all 6 talons
        self.myRobot.setExpiration(0.1) #safety expiration of 10ms / 5ms without signal before stopping
    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True) #safety first
    def teleopPeriodic(self):
        self.myRobot.tankDrive(self.stick.getX(), self.stick.getY()) #simple x^2 throttle curve
        #self.myRobot.tankDrive(self.leftStick.getY()**2 * -1, self.rightStick.getY()**2 * -1) #for two joystick control
if __name__ == "__main__":
	wpilib.run(MyRobot)
