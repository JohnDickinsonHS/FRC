try:
    import wpilib
except:
    from pyfrc import wpilib
import time

#Hardware setup
stick = wpilib.Joystick(1)
leftmotor = wpilib.Jaguar(1)
rightmotor = wpilib.Jaguar(2)
leftarmmotor = wpilib.Victor(3)
rightarmmotor = wpilib.Victor(4)

#Program variables
armpos = 0

#Manually-called functions
def movearm(power):
    if(!starttime):
        starttime = time.time()
    else:
        if(power > 0):
            armpos += time.time() - starttime
        elif(power < 0):
            armpos -= time.time() - starttime
    if(armpos != 1) and (armpos != -1) and (abs(throttle)-15 > 0):
        leftarmmotor.Set(power)
        rightarmmotor.Set(power)



#Competition-called code        
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
        throttle = stick.GetThrottle()
        # Motor control
        leftmotor.Set((-stickY)+stickX)
        rightmotor.Set((-stickY)-stickX)
        movearm(throttle)
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