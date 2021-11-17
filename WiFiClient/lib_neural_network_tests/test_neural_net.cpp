#include "math.h"

#include <iostream>
#include <cassert>
#include "neural_network.h"


using namespace std;

void print_value(TransferValues * tv){
  for (int i = 0; i < tv->len; i++){
    cout << tv->values[i] << " ";
  }
}

void test_fully_connected(){
  float w0raw []{1,2,3,4,5,6};
  Params w0 = {0, 6, w0raw };
  float b0raw []{1,2,3};
  Params b0 = {0, 3, b0raw };
  
  float inputs_raw[]{1,2};
  TransferValues input{2, inputs_raw};

  FullyConnected fc(3,w0,b0);
  TransferValues * result = fc.compute(&input);

  assert((result->values[0]) == 6 && (result->values[2] == 20));
  cout << "fc works" << endl;
}

void test_relu(){
  float inputs_raw[]{-1,3,4};
  TransferValues input{3, inputs_raw};

  Relu relu(3);
  TransferValues * result = relu.compute(&input);

  assert((result->values[0]) == 0 && (result->values[2] == 4));
  
  cout << "relu works" << endl;

}  

void test_tanh(){

  float inputs_raw[]{-1,3,4, 10, -10, 1000, -1000};
  TransferValues input{7, inputs_raw};

  Tanh tanh(7);
  TransferValues * result = tanh.compute(&input);

  float t[]{-0.7616,  0.9951,  0.9993, 1, -1, 1, -1};
  assert(result->nearly_equals(t));
  cout << "tanh works" << endl;
  print_value(result);

}
  
void test_neural_network(){
  float w0_raw[]{1,2,3,4,5,6};
  Params w0 = {0, 6, w0_raw};
  float b0_raw[]{1,2,3};
  Params b0 = {0, 3, b0_raw};
  float w1_raw[]{1,2,3,4,5,6};
  float b1_raw[]{1,2};
  Params w1 = {0, 6, w1_raw };
  Params b1 = {0, 2, b1_raw };

  FullyConnected fc1{3, w0, b0};
  Relu relu1(3);
  FullyConnected fc2{2, w1, b1};
  Tanh ta(2);
  Stage * stages [] = {&fc1, &relu1, &fc2, &ta};

  NeuralNetwork nn = {sizeof(stages)/sizeof(Stage*), stages};

  float input_raw[]{1,2};
  TransferValues input_values{2, input_raw};

  TransferValues * result = nn.compute(&input_values);
  
  cout << "neural network works" << endl;
}

int main(){
  test_fully_connected();
  test_relu();
  test_tanh();
  test_neural_network();
  return 0;
}
