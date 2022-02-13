#include <neural_network.h>
#include "weight_definition.h"

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

class Neural_Controller{
  float previous_error,commulative_error;
  
public:
  Neural_Controller(): previous_error(0), commulative_error(0){};
  
  TransferValues * control(float & lpower,float & rpower, float * ypr, float distance_to_target, float radius_to_target){
      
    float ypr1 = ypr[1];
    
    float error = ypr1;
    float delta_error = error - previous_error;
    commulative_error *= 0.99;
    commulative_error += error;
    inputs.values[0] = error;
    inputs.values[1] = commulative_error;
    inputs.values[2] = delta_error;
    previous_error = error;

    TransferValues * result = nn.compute(&inputs);
    lpower = result->values[0]*500;
    rpower = result->values[1]*500;
    return result;
  }
};

class WeightParamsUpdater{
  const int weight_params_count;
  const Params ** weight_params;
  
  public:
  WeightParamsUpdater(const int weight_params_count, const Params ** weight_params):
  weight_params_count(weight_params_count), weight_params(weight_params) {}
  
  void from_request(const String & requestMessage){
    
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, requestMessage);
    mqttclient.publish("robot/param_update_debug", String("recieved " )+ requestMessage); 
    
    
    int id = doc["param_id"];
    int param_start_offset = doc["param_start_offset"];
    
    mqttclient.publish("robot/param_update_debug", String("updating " )+ id + " from location " + param_start_offset ); 
    
    for(int i = 0; i < weight_params_count; i++){
      if(id == weight_params[i]->class_id){
    
        JsonArray arr = doc["param_values"].as<JsonArray>();
        JsonArray::iterator it=arr.begin();
        mqttclient.publish("robot/param_update_debug", String("size of array") +arr.size() ); 
        
        for(int k = param_start_offset; it!=arr.end() && k < weight_params[i]->len; ++it, ++k){
          weight_params[i]->values[k] = it->as<float>();
          mqttclient.publish("robot/param_update_debug", String("setting value") + i + " " + k + " to " + weight_params[i]->values[k]); 
        }    
      }
    }
  }
};

const Params * weight_params[] = {&mu_0_weight_params,&mu_0_bias_params,&mu_2_weight_params,&mu_2_bias_params, &mu_4_weight_params, &mu_4_bias_params};
WeightParamsUpdater params_updater(NUM(weight_params),weight_params);
