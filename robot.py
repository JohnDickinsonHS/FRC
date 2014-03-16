try:
    import wpilib
except:
    from pyfrc import wpilib

#Hardware setup
stick = wpilib.Joystick(1)
leftmotor = wpilib.Jaguar(1)
rightmotor = wpilib.Jaguar(2)
leftarmmotor = wpilib.Victor(3)
rightarmmotor = wpilib.Victor(4)
tensionmotor = wpilib.Jaguar(5)
release = wpilib.Servo(6)
ds = wpilib.DriverStation.GetInstance()

#Manually-called functions
def movearm(power):
    leftarmmotor.Set(power)
    rightarmmotor.Set(power)

#Competition-called code        
def checkRestart():
    if stick.GetRawButton(7):
        raise RuntimeError("Restart")

def disabled():
    while wpilib.IsDisabled():
        '''if(ds.GetDigitalIn(1)):

        '''
        checkRestart()
        wpilib.Wait(0.01)

def autonomous():
    wpilib.GetWatchdog().SetEnabled(False)
    leftmotor.Set(25)
    rightmotor.Set(25)
    wpilib.Wait(4)
    leftmotor.Set(0)
    rightmotor.Set(0)
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
        stickX = -stick.GetX()
        # Motor control
        leftmotor.Set((-stickY)+stickX)
        rightmotor.Set((-stickY)-stickX)
        if(stick.GetRawButton(11)):
            movearm(1)
        elif(stick.GetRawButton(12)):
            movearm(-10)
        else:
            movearm(0)
        if(stick.GetRawButton(2)):
            tensionmotor.Set(25)
        else:
            tensionmotor.Set(0)
        if(stick.GetRawButton(1)):
            release.Set(1.0)
            wpilib.Wait(0.5)
            release.Set(0.0)
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