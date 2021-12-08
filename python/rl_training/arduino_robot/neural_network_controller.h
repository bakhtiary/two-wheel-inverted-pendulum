#include <neural_network.h>
#include "weight_definitions.h"

const int FIRST_LAYER_SIZE = mu_0_bias_params.len;
const int SECOND_LAYER_SIZE = mu_2_bias_params.len;
const int THIRD_LAYER_SIZE = mu_4_bias_params.len;


FullyConnected fc1{FIRST_LAYER_SIZE, mu_0_weight_params, mu_0_bias_params};
Relu relu1(FIRST_LAYER_SIZE );
FullyConnected fc2{SECOND_LAYER_SIZE, mu_2_weight_params, mu_2_bias_params};
Relu relu2(SECOND_LAYER_SIZE);
FullyConnected fc3{THIRD_LAYER_SIZE, mu_4_weight_params, mu_4_bias_params};
Tanh ta(THIRD_LAYER_SIZE);
Stage * stages [] = {&fc1, &relu1, &fc2, &relu2, &fc3, &ta};
TransferValues inputs{NUM(input_holder), input_holder};
NeuralNetwork nn = {NUM(stages), stages};

class NN_Controller{
  Motor & motor1;
  Motor & motor2;
  float max_motor_power = 260;
public:
  NN_Controller(Motor & motor1, Motor & motor2):motor1(motor1),motor2(motor2){};
  void control(float * ypr, float distance_to_target, float radius_to_target){
    // keep last times events:
    inputs.values[0] = inputs.values[3];
    inputs.values[1] = inputs.values[4];
    inputs.values[2] = inputs.values[5];

    // current errors:
    inputs.values[3] = ypr[0];
    inputs.values[4] = ypr[1];
    inputs.values[5] = ypr[2];

    // delta errors:
    inputs.values[6] = ypr[0] - inputs.values[0];
    inputs.values[7] = ypr[1] - inputs.values[1];
    inputs.values[8] = ypr[2] - inputs.values[2];

    // commulative errors scaling to zero
    float scaling_factor = 0.999;
    inputs.values[9] *= scaling_factor;
    inputs.values[10] *= scaling_factor;
    inputs.values[11] *= scaling_factor;

    // commulative errors
    inputs.values[9] += ypr[0];
    inputs.values[10] += ypr[1];
    inputs.values[11] += ypr[2];

    TransferValues * result = nn.compute(&inputs);
    
    motor1.setPower(result->values[0]*max_motor_power);
    motor2.setPower(result->values[1]*max_motor_power);
  }
};
