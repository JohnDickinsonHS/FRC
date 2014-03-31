try:
    import wpilib
except ImportError:
    print('Failed to import WPILib. Attempting to run in pyFRC simulator..')
    try:
        from pyfrc import wpilib
    except ImportError:
        print('Failed to import pyFRC. Exiting.')
        raise SystemExit

#Hardware setup
stick = wpilib.Joystick(1)
leftmotor = wpilib.Jaguar(1)
rightmotor = wpilib.Jaguar(2)
armwinch = wpilib.Jaguar(5)
tensionwinch = wpilib.Victor(6)
release = wpilib.Servo(7)
ds = wpilib.DriverStation.GetInstance()

#Manually-called functions
def motors(motors, power):
    if type(motors) is list:
        for motor in motors:
            motor.Set(power)
    else:
        print('Motors function should be called with a list.')

#Competition-called code        
def checkRestart():
    if stick.GetRawButton(7):
        raise RuntimeError('Restart')

def disabled():
    while wpilib.IsDisabled():
        '''if(ds.GetDigitalIn(1)):

        '''
        checkRestart()
        wpilib.Wait(0.01)

def autonomous():
    wpilib.GetWatchdog().SetEnabled(False)
    motors([leftmotor,rightmotor],25)
    wpilib.Wait(1)
    motors([leftmotor,rightmotor],0)
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
        if stick.GetRawButton(11): #arm down
            armwinch.Set(25)
        elif stick.GetRawButton(12): #arm up
            armwinch.Set(-25)
        else: #stop winding arm
            armwinch.Set(0)
        if(stick.GetRawButton(2)): #wind up plunger
            tensionwinch.Set(25)
        else: #stop winding
            tensionwinch.Set(0)
        if(stick.GetRawButton(1)): #move servo
            release.Set(1.0)
            wpilib.Wait(0.5)
            release.Set(0.0)
        wpilib.Wait(0.04)
def run():
    '''Main loop'''
    while 1:
        if wpilib.IsDisabled():
            print('Running disabled()')
            disabled()
            while wpilib.IsDisabled():
                wpilib.Wait(0.01)
        elif wpilib.IsAutonomous():
            print('Running autonomous()')
            autonomous()
            while wpilib.IsAutonomous() and wpilib.IsEnabled():
                wpilib.Wait(0.01)
        else:
            print('Running teleop()')
            teleop()
            while wpilib.IsOperatorControl() and wpilib.IsEnabled():
                wpilib.Wait(0.01)

if __name__ == '__main__':
    wpilib.run()