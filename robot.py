try:
    import wpilib
except:
    from pyfrc import wpilib

stick = wpilib.Joystick(1)

leftmotor = wpilib.Jaguar(1)
rightmotor = wpilib.Jaguar(2)
launcher_tension = wpilib.Jaguar(3)

def checkRestart():
    if stick.GetRawButton(10):
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
        stickY = stick.GetY()
        stickX = stick.GetX()
        # Motor control
        leftmotor.Set((-stickY)+stickX)
        rightmotor.Set((-stickY)-stickX)
        if stick.GetRawButton(2):
            launcher_tension.Set(128)
        else:
            launcher_tension.Set(0)
        '''if stick.GetRawButton(1):
            release launcher tension'''
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