import wpilib

global digitalState
stick1 = wpilib.Joystick(1)
ds = wpilib.DriverStation.GetInstance()

#User-defined functions
def checkDsInput():
    if ds.getDigitalIn(1):
        digitalState = 1
    elif ds.getDigitalIn(2):
        digitalState = 2
    #and so on and so on and so on.

def customAutonomous(num):
    if num == 1:
        pass #replace this with autonomous routine one
    elif num == 2:
        pass #ditto
    #and so on and so on and so on.

#Competition-called code
def checkRestart():
    if stick1.GetRawButton(10):
        raise RuntimeError("Restart")

def disabled():
    while wpilib.IsDisabled():
        checkRestart()
        checkDsInput()
        wpilib.Wait(0.01)

def autonomous():
    while wpilib.IsAutonomous() and wpilib.IsEnabled():
        customAutonomous(digitalState)
        checkRestart()
        wpilib.Wait(0.01)

def teleop():
    while wpilib.IsOperatorControl() and wpilib.IsEnabled():
        checkRestart()
        wpilib.Wait(0.01)

def run():
    """Main loop"""
    while 1:
        if wpilib.IsDisabled():
            print("Running disabled()")
            disabled()
            while wpilib.IsDisabled():
                wpilib.Wait(0.01)
        elif wpilib.IsAutonomous():
            print("Running autonomous()")
            autonomous()
            while wpilib.IsAutonomous() and wpilib.IsEnabled():
                wpilib.Wait(0.01)
        else:
            print("Running teleop()")
            teleop()
            while wpilib.IsOperatorControl() and wpilib.IsEnabled():
                wpilib.Wait(0.01)

