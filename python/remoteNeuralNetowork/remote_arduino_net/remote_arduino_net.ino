
#include <robotics_config.h>
#include <neural_network.h>
#include "remote_network.pb.h"
#include "weight_definitions.h"

#include <WiFi.h>
#include "EspMQTTClient.h"

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

class WeightParamsUpdater{
  const int weight_params_count;
  const Params ** weight_params ;
  public:
  WeightParamsUpdater(const int weight_params_count, const Params ** weight_params):
  weight_params_count(weight_params_count), weight_params(weight_params) {}
  void from_request(RemoteNetwork_ModelUpdateRequest & requestMessage){
    int id = requestMessage.param_id;
    Serial.println(String("updating " )+ id + " from location " + requestMessage.param_start_offset + " with len " + requestMessage.param_values.values_count);
    for(int i = 0; i < weight_params_count; i++){
      if(id == weight_params[i]->class_id){
        for(int j = 0, k = requestMessage.param_start_offset; j < requestMessage.param_values.values_count && k < weight_params[i]->len; j++, k++){
          weight_params[i]->values[k] = requestMessage.param_values.values[j];
        }    
      }
    }
  }
};

const Params * weight_params[] = {&mu_0_weight_params,&mu_0_bias_params,&mu_2_weight_params,&mu_2_bias_params, &mu_4_weight_params, &mu_4_bias_params};

WeightParamsUpdater params_updater(NUM(weight_params),weight_params);

EspMQTTClient client(
  ssid,
  password,
  host_ip,  // MQTT Broker server ip
  0,   // Can be omitted if not needed
  0,   // Can be omitted if not needed
  "TestClient",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
}


uint8_t output_buffer[600]; //600 is 512 rounded to the highest 100. We might have 128 float for which we will need 512 bytes and then some extra for the overhead.

void onConnectionEstablished() // This function is called once everything is connected (Wifi and MQTT) // WARNING : YOU MUST IMPLEMENT IT IF YOU USE EspMQTTClient
{
  // Subscribe to "mytopic/test" and display received message to Serial
  client.subscribe("evaluation_request", [](uint8_t* payload, unsigned int message_length) {
    RemoteNetwork_ModelEvaluationRequest message = RemoteNetwork_ModelEvaluationRequest_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(payload, message_length);
    bool status = pb_decode(&stream, RemoteNetwork_ModelEvaluationRequest_fields, &message);

    Serial.println(message.input_values.values[0]);
    for (int i = 0; i < message.input_values.values_count; i++){
      inputs.values[i] = message.input_values.values[i];
    }

    TransferValues * result = nn.compute(&inputs);
    Serial.print("value 0 is ");
    Serial.println(result->values[0]);

    RemoteNetwork_ModelEvaluationResponse response_message = RemoteNetwork_ModelEvaluationResponse_init_zero;
    
    /* Create a stream that will write to our buffer. */
    pb_ostream_t response_stream = pb_ostream_from_buffer(output_buffer, sizeof(output_buffer));
    
    for (int i = 0; i < result->len; i++){
      response_message.output_values.values[i] = result->values[i];
    }

    response_message.output_values.values_count = result->len;
     
    
    /* Now we are ready to encode the message! */
    status = pb_encode(&response_stream, RemoteNetwork_ModelEvaluationResponse_fields, &response_message);
    int response_length = response_stream.bytes_written;
    client.publishRaw("evaluation_result", output_buffer, response_length, false); // You can activate the retain flag by setting the third parameter to true
    
  });

  client.subscribe("model_update_request", [](uint8_t* payload, unsigned int message_length) {
    RemoteNetwork_ModelUpdateRequest message = RemoteNetwork_ModelUpdateRequest_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(payload, message_length);
    bool status = pb_decode(&stream, RemoteNetwork_ModelUpdateRequest_fields, &message);
    params_updater.from_request(message);
  }, 1);

  // Subscribe to "mytopic/wildcardtest/#" and display received message to Serial
  client.subscribe("mytopic/wildcardtest/#", [](const String & topic, const String & payload) {
    Serial.println("(From wildcard) topic: " + topic + ", payload: " + payload);
  });

  // Publish a message to "mytopic/test"
  client.publish("mytopic/test", "This is a message"); // You can activate the retain flag by setting the third parameter to true

  // Execute delayed instructions
  client.executeDelayed(5 * 1000, []() {
    client.publish("mytopic/wildcardtest/test123", "This is a message sent 5 seconds later");
  });
}

void loop() {
  client.loop();
}
