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
  EspMQTTClient & client;
  float previous_error,commulative_error;
  
public:
  NN_Controller( EspMQTTClient & client):  client(client), previous_error(0), commulative_error(0){};
  TransferValues * control(float * ypr, float distance_to_target, float radius_to_target){
      
      float ypr1 = ypr[1];
      
      float error = ypr1;
      float delta_error = error - previous_error;
      commulative_error *= 0.99;
      commulative_error += error;
      inputs.values[0] = error;
      inputs.values[1] = commulative_error;
      inputs.values[2] = delta_error;
      previous_error = error;

    
    // keep last times events:
//    inputs.values[0] = inputs.values[3];
//    inputs.values[1] = inputs.values[4];
//    inputs.values[2] = inputs.values[5];
//
//    // current errors:
//    inputs.values[3] = ypr[0];
//    inputs.values[4] = ypr[1]; 
//    inputs.values[5] = ypr[2];
//
//    // delta errors:
//    inputs.values[6] = ypr[0] - inputs.values[0];
//    inputs.values[7] = ypr[1] - inputs.values[1];
//    inputs.values[8] = ypr[2] - inputs.values[2];

    // commulative errors scaling to zero
//    float scaling_factor = 0.999;
//    inputs.values[9] *= scaling_factor;
//    inputs.values[10] *= scaling_factor;
//    inputs.values[11] *= scaling_factor;
//
//    // commulative errors
//    inputs.values[9] += ypr[0];
//    inputs.values[10] += ypr[1];
//    inputs.values[11] += ypr[2];

    TransferValues * result = nn.compute(&inputs);
    return result;

//    client.publish("robot/neural_net_pid", String("  P ") + error + " I " + commulative_error + " D " + delta_error + " rpower: " + rpower + " lpower: " + lpower + " inference_duration "  + delta_time + " start_time " + start_time );
//    client.publish("robot/fc1_inputs", String(" values: ") +  inputs.toString() + " time " + millis() );
//    client.publish("robot/fc1_weights", String(" values: ") + fc1.weights.toString() + " time " + millis() );
//    client.publish("robot/fc1_outputs", String(" values: ") + fc1.output->toString() + " time " + millis() );
//    client.publish("robot/fc2_weights", String(" values: ") + fc2.weights.toString() + " time " + millis() );
//    client.publish("robot/fc2_outputs", String(" values: ") + fc2.output->toString() + " time " + millis() );
//    client.publish("robot/fc3_weights", String(" values: ") + fc3.weights.toString() + " time " + millis() );
//    client.publish("robot/fc3_outputs", String(" values: ") + fc3.output->toString() + " time " + millis() );
    
  }
};
