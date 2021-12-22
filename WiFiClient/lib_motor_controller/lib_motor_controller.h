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
    digitalWrite(pin2, power<0?HIGH:LOW);

    int appliedPower = constrain(abs(power) + low_power_offset, 0, 255);

//    Serial.println(String("applied_power")+appliedPower);
    ledcWrite(ledchannel_id, appliedPower);
//   analogWrite(enpin, appliedPower);

  }
};
