#include "robotics_config.h"

struct Stage{
};

struct Params {

    int class_id;  
    int len_of_data;
    float * param_data;
};

Params w0 = {0, 4, ((float []) {1,2,3,4,5,6}) };
Params b0 = {0, 4, ((float []) {1,2,3}) };

Params w1 = {0, 4, ((float []) {1,2,3,4,5,6}) };
Params b1 = {0, 4, ((float []) {1,2}) };


struct FullyConnected: public Stage
{
  int input_size;
  int output_size;
  Params & weights;
  Params & biases;

  FullyConnected(
    int input_size,
    int output_size,
    Params & weights,
    Params & biases
  ): input_size(input_size), output_size(output_size), weights(weights), biases(biases){}
  
};

class Relu: public Stage{

};

class Tanh: public Stage{

};


class NeuralNetwork{
  public:
  Stage * stages;
  int len_stages;
};

FullyConnected fc1{2, 3, w0, b0};
Relu relu1;
FullyConnected fc2{3, 2, w1, b1};
Tanh ta;
Stage stages [] = {fc1, relu1, fc2, ta};


NeuralNetwork nn = {stages, sizeof(stages)};


void setup() {
  
}

void loop() {
  // put your main code here, to run repeatedly:
  nn.compute({1.0,1.0});
}
