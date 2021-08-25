
//    FILE: GY521_pitch_roll_yaw.ino
//  AUTHOR: Rob Tillaart
// VERSION: 0.1.0
// PURPOSE: demo PRY
//    DATE: 2020-08-06

#include <Wire.h>

uint32_t counter = 0;

int sign(int x){
  return (x > 0) - (x < 0);
}

class Motor{
  public:
  int pin1;
  int pin2;
  int enpin;
  int ledchannel_id;
  float current_power = 0;
  int last_switch = 0;
  int low_power_offset = 0 ;
  int last_dir = 0;
  Motor(int p1, int p2, int _enpin, int _ledchannel_id, int _low_power_offset){
    pin1 = p1;
    pin2 = p2;
    ledchannel_id = _ledchannel_id;
    enpin = _enpin;
    
    low_power_offset = _low_power_offset;
  }
  void enable(){
    pinMode(pin1, OUTPUT);
    pinMode(pin2, OUTPUT);
   // pinMode(enpin, OUTPUT);
    ledcAttachPin(enpin, ledchannel_id);
    ledcSetup(ledchannel_id, 12000, 8); // 12 kHz PWM, 8-bit resolution
  }
  void setPower(int power){
   
    digitalWrite(pin1, power>0?HIGH:LOW);
    digitalWrite(pin2, power<=0?HIGH:LOW);
    
    int appliedPower = constrain(abs(power) + low_power_offset, 0, 255);

    Serial.println(String("applied_power")+appliedPower);
    ledcWrite(ledchannel_id, appliedPower);
//   analogWrite(enpin, appliedPower);
 
  }
};

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
