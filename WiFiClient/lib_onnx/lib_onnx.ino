#include "robotics_config.h"
#include "neural_network.h"

Params w0 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b0 = {0, 3, ((float []) {1,2,3}) };

Params w1 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b1 = {0, 2, ((float []) {1,2}) };



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
