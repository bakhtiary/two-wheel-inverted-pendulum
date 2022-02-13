#include <lib_motor_controller.h>

Motor motor1 = Motor(25,33,32,1,140);
Motor motor2 = Motor(26,27,14,2,140);  

void setupMotors(){  
  motor1.enable();
  motor2.enable();
}

void moveMotors(float lpower, float rpower){
  motor1.setPower(lpower);
  motor2.setPower(rpower);
}
