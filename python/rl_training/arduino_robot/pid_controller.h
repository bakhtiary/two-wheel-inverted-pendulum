struct Control_Data{
  float proportional;
  float integration;
  float derivative;
  float minimal_motor_power;
  float offset;
  float delay_time;
  String get_string(){
    return String("proportional, integration, derivative, min_power, offset, delay_time +\n") + proportional + "," + integration + "," + derivative + "," + minimal_motor_power + "," + offset + "," + delay_time;
  }
};


class Pid_Controller{
  Control_Data & control_data;
  Motor & motor1;
  Motor & motor2;
  float previous_error,commulative_error;

public:
  
  Pid_Controller(Control_Data & control_data, Motor & motor1, Motor & motor2):
  control_data(control_data), motor1(motor1), motor2(motor2), previous_error{0} ,commulative_error{0} {}
  void control(float ypr1){
      float error = ypr1 + control_data.offset;
      float delta_error = error - previous_error;
      commulative_error *= 0.99;
      commulative_error += error;

      float power = error*control_data.proportional + commulative_error*control_data.integration + delta_error*control_data.derivative;
      motor1.setPower(power);
      motor2.setPower(power);

      previous_error = error;
    
  }
  
};
