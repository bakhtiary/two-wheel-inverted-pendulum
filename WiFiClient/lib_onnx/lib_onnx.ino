#include "robotics_config.h"

struct TransferValues{
  int len_of_data;
  float * values;
};

struct Stage{
  public:
  int output_size;
  TransferValues * output;
  Stage(int output_size): output_size(output_size){
  output = new TransferValues{output_size, new float [output_size]};  
  }
};

struct Params {

    int class_id;  
    int len_of_data;
    float * param_data;
};

Params w0 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b0 = {0, 3, ((float []) {1,2,3}) };

Params w1 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b1 = {0, 2, ((float []) {1,2}) };


struct FullyConnected: public Stage
{
  int input_size;
  int output_size;
  Params & weights;
  Params & biases;
  TransferValues * output;

  FullyConnected(
    int input_size,
    int output_size,
    Params & weights,
    Params & biases
  ): input_size(input_size), Stage(output_size), weights(weights), biases(biases){
    
  }
  
};

class Relu: public Stage{
  public:
  Relu(int output_size):Stage(output_size){}
};

class Tanh: public Stage{
  public:
  Tanh(int output_size):Stage(output_size){}
};


class NeuralNetwork{
  public:
  int len_stages;
  Stage * stages;
  TransferValues * compute(TransferValues * values){
    
    for (int i = 0; i < len_stages; i++){
      stages[i] =       
    }
    return stages[len_stages-1].output;
  }
};

FullyConnected fc1{2, 3, w0, b0};
Relu relu1(3);
FullyConnected fc2{3, 2, w1, b1};
Tanh ta(2);
Stage stages [] = {fc1, relu1, fc2, ta};


NeuralNetwork nn = {sizeof(stages), stages};
TransferValues InputValues = {2, ((float []) {1,2})};

void setup() {
  Serial.begin(115200);
  Serial.println("setting up");
}

void loop() {
  // put your main code here, to run repeatedly:
  TransferValues * result = nn.compute(&InputValues);
  Serial.println("connecting to wifi:");
  delay(1);

}
