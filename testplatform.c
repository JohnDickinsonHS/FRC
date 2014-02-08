#pragma config(Hubs,  S1, HTMotor,  none,     none,     none)
#pragma config(Sensor, S1,     ,               sensorI2CMuxController)
#pragma config(Motor,  mtr_S1_C1_1,     leftMotor,     tmotorTetrix, openLoop)
#pragma config(Motor,  mtr_S1_C1_2,     rightMotor,    tmotorTetrix, openLoop)
//*!!Code automatically generated by 'ROBOTC' configuration wizard               !!*//

/*
THIS CODE IS DESIGNED TO MIRROR THE FRC BOT'S CONTROL SYSTEMS FOR DRIVING PRACTICE
*/
#include "JoystickDriver.c"  //Include file to "handle" the Bluetooth messages.
int stickY;
int stickX;

task main(){
  while (true)
  {
  	stickY = joystick.joy1_y1;
  	stickX = joystick.joy1_x1;
  	motor[leftMotor] = (stickY * -1)+stickX;
  	motor[rightMotor] = (stickY * -1)-stickX;
  }
}
