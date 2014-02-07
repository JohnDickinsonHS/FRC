try:
    import wpilib
except:
    from pyfrc import wpilib
#import math

lstick = wpilib.Joystick(1)

leftmotor = wpilib.Jaguar(1)
rightmotor = wpilib.Jaguar(2)

leftdrivefudge = 1.2125

def checkRestart():
    if lstick.GetRawButton(10):
        raise RuntimeError("Restart")

def disabled():
    while wpilib.IsDisabled():
        checkRestart()
        wpilib.Wait(0.01)

def autonomous():
    wpilib.GetWatchdog().SetEnabled(False)
    while wpilib.IsAutonomous() and wpilib.IsEnabled():
        checkRestart()
        wpilib.Wait(0.01)

def teleop():
    dog = wpilib.GetWatchdog()
    dog.SetEnabled(True)
    dog.SetExpiration(0.25)
    while wpilib.IsOperatorControl() and wpilib.IsEnabled():
        dog.Feed()
        checkRestart()
        stickX = lstick.getX()
        stickY = lstick.getY()
        if stickX > 0:
            rightY = ((stickY * -1)+'''math.abs'''(stickX))/2
            leftY = stickY * (-1 * leftdrivefudge)
        if stickX < 0:
            leftY = (stickY * (-1 * leftdrivefudge)+'''math.abs'''(stickX))/2
            rightY = stickY * -1
        # Motor control
        leftmotor.Set(leftY)
        rightmotor.Set(rightY)
        wpilib.Wait(0.04)

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

if __name__ == "__main__":
    wpilib.run()