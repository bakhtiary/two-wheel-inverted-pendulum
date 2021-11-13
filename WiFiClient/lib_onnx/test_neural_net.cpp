#include "math.h"
#include "neural_network.h"

#include <iostream>
#include <cassert>

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

void   test_relu(){
  float inputs_raw[]{-1,3,4};
  TransferValues input{3, inputs_raw};

  Relu relu(3);
  TransferValues * result = relu.compute(&input);

  print_value(result);
  assert((result->values[0]) == 0 && (result->values[2] == 4));
  
  cout << "relu works" << endl;

}  

void test_tanh(){

  float inputs_raw[]{-1,3,4};
  TransferValues input{3, inputs_raw};

  Tanh tanh(3);
  TransferValues * result = tanh.compute(&input);

  float t[]{-0.7616,  0.9951,  0.9993};
  assert(result->nearly_equals(t));
  cout << "tanh works" << endl;

}
  

int main(){
  test_fully_connected();
  test_relu();
  test_tanh();
  std::cout << "test" << std::endl;
  return 0;
}
