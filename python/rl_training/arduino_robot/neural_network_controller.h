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
public:
  NN_Controller(Motor & motor1, Motor & motor2):motor1(motor1),motor2(motor2){};
  void control(float * ypr){
    
  }
};
