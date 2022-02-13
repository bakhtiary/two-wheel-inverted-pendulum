
struct Control_Coeffs{
public:
  float proportional;
  float integration;
  float derivative;
};

class Pid_Controller{
  Control_Coeffs coeffs;
  float previous_error,commulative_error;

public:
  Pid_Controller():
  coeffs{650.0, 5.0, 600.0}, previous_error(0) ,commulative_error(0) {}
  float control(float ypr1){
      float error = ypr1;
      float delta_error = error - previous_error;
      commulative_error *= 0.99;
      commulative_error += error;

      float power = error*coeffs.proportional + commulative_error*coeffs.integration + delta_error*coeffs.derivative;
      previous_error = error;
      return power; 
  }
};
