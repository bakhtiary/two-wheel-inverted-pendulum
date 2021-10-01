
#include <Wire.h>
#include "lib_motor_controller.h"

uint32_t counter = 0;

Motor motor1 = Motor(26,27,25,1,60);
Motor motor2 = Motor(12,14,13,2,60);

void setup()
{
  motor1.enable();
  motor2.enable();

  Serial.begin(115200);
  Serial.println(__FILE__);

  Wire.begin();

  delay(100);

  Serial.println("start...");

  // set callibration values from calibration sketch.
}

void loop()
{

  motor1.setPower(250);
  motor2.setPower(250);
  delay(1000);
  motor1.setPower(-251);
  motor2.setPower(-251);
  delay(1000);

  counter++;
}
