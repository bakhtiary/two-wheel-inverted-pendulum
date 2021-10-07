struct Sending_data{
  unsigned long sequence_id;
  unsigned long control_start_time;
  unsigned long control_end_time;
  float power;
};

struct Control_data{
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
