#include "robotics_config.h"

struct TransferValues{
  int len;
  float * values;
};

struct Stage{
  public:
  TransferValues * output;
  Stage(int output_size){
  output = new TransferValues{output_size, new float [output_size]};  
  }
  TransferValues * compute(TransferValues * input){};
};

struct Params {

    int class_id;  
    int len;
    float * values;
};

Params w0 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b0 = {0, 3, ((float []) {1,2,3}) };

Params w1 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b1 = {0, 2, ((float []) {1,2}) };


struct FullyConnected: public Stage
{
  int input_size;
  Params & weights;
  Params & biases;
  TransferValues * output;

  FullyConnected(
    int output_size,
    Params & weights,
    Params & biases
  ): Stage(output_size), weights(weights), biases(biases){}

  TransferValues * compute(TransferValues * input){
    for (int i = 0; i < output->len; i++){
      output->values[i] = biases.values[i];
      for (int j = 0; j < input->len; j++){
        output->values[i] += input->values[j]*weights.values[j + i * input->len];
      }
    }
    return output;
  };

  
};

class Relu: public Stage{
  public:
  Relu(int output_size):Stage(output_size){}
  TransferValues * compute(TransferValues * input){
    for (int i = 0; i < input->len; i++){
      float cur_val = input->values[i];
      output->values[i] = cur_val < 0 ? 0 : cur_val;
    }
    return output;
  }
};

class Tanh: public Stage{
  public:
  Tanh(int output_size):Stage(output_size){}
  TransferValues * compute(TransferValues * input){
    return output;
  }
};


class NeuralNetwork{
  public:
  int len_stages;
  Stage * stages;
  TransferValues * compute(TransferValues * values){
    Serial.println(len_stages);
    for (int i = 0; i < len_stages; i++){
      values = stages[i].compute(values);
      Serial.println(i);
    }
    return values;
  }
};

FullyConnected fc1{3, w0, b0};
Relu relu1(3);
FullyConnected fc2{2, w1, b1};
Tanh ta(2);
Stage stages [] = {fc1, relu1, fc2, ta};

NeuralNetwork nn = {sizeof(stages)/sizeof(Stage*), stages};


TransferValues InputValues{2, ((float []) {1,2})};

void setup() {
  Serial.begin(115200);
  Serial.println("setting up");
}

void loop() {
  
  TransferValues * result = nn.compute(&InputValues);
  Serial.println(String("result is ") + result->values[0] + " " + result->values[1]);
  delay(1000);

  

}
