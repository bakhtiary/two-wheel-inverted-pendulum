#include <robotics_config.h>
#include <remote_registry.h>
#include <neural_network.h>
#include "neural_comm_data.h"

Params w0 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b0 = {0, 3, ((float []) {1,2,3}) };

Params w1 = {0, 6, ((float []) {1,2,3,4,5,6}) };
Params b1 = {0, 2, ((float []) {1,2}) };


FullyConnected fc1{3, w0, b0};
Relu relu1(3);
FullyConnected fc2{2, w1, b1};
Tanh ta(2);
Stage * stages [] = {&fc1, &relu1, &fc2, &ta};

CommunicationChannel communication_channel{host_ip, host_port, 20};

NeuralNetwork nn = {sizeof(stages)/sizeof(Stage*), stages};

template <int INPUT_SIZE, int OUTPUT_SIZE>
class Remote_Model_Loader{
  public:
    NeuralNetwork & neural_network;
    CommunicationChannel & communication_channel;
    OutputGram<INPUT_SIZE> input_gram;
    OutputGram<OUTPUT_SIZE> output_gram;
    WeightGram weight_gram;
    Remote_Model_Loader(
      NeuralNetwork & neural_network, CommunicationChannel & communication_channel):
    neural_network(neural_network), communication_channel(communication_channel){
      communication_channel.register_data(&input_gram, sizeof(input_gram));    
      communication_channel.register_data(&weight_gram, sizeof(weight_gram));    
    };
    
    void recieve_message(CommunicationData * comm_data){
      if (comm_data->id == input_gram.id){ // input gram
        TransferValues inputValues{input_gram.float_payload_len, input_gram.payload};
        TransferValues * result = neural_network.compute(&inputValues);
        for(int i = 0; i < result->len; i++){
          output_gram.payload[i] = result->values[i];
        }
        communication_channel.send_data(output_gram,sizeof(output_gram));
      }
    }
};

Remote_Model_Loader <3,2> rml(nn,communication_channel);

void setup() {
  Serial.begin(115200);
  Serial.println("connecting wifi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.print("WiFi connected. ");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  communication_channel.init();
}


void loop() {
    delay(500);

    CommunicationData * updated_value = communication_channel.update_registers();
    
    if (updated_value != 0){
      Serial.println("updated control data " + updated_value->toString());
      rml.recieve_message(updated_value);
    }
}
