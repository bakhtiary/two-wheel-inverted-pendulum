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
  EspMQTTClient & client;
  float previous_error,commulative_error;
  int step_count;

public:
  
  Pid_Controller(Control_Data & control_data, EspMQTTClient & client):
  control_data(control_data), client(client), previous_error(0) ,commulative_error(0), step_count(0) {}
  float control(float ypr1){
      float error = ypr1 + control_data.offset;
      float delta_error = error - previous_error;
      commulative_error *= 0.99;
      commulative_error += error;

      float power = error*control_data.proportional + commulative_error*control_data.integration + delta_error*control_data.derivative;
      client.publish("robot/pid_result", String(" ypr: ") + ypr1 + " P " + error + " I " + commulative_error + " D " + delta_error + " power: " + power + " time " + millis() );
      previous_error = error;
      return power;
    
  }
  
};
