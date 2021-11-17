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

CommunicationChannel<10> communication_channel{host_ip, host_port};

NeuralNetwork nn = {sizeof(stages)/sizeof(Stage*), stages};

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

InputGram input;

TransferValues inputValues{2, ((float []) {1,2})};

void loop() {
    delay(500);
    TransferValues * result = nn.compute(&inputValues);
    Serial.println(result->toString());

    CommunicationData * updated_value = communication_channel.update_registers();
    
    if (updated_value != 0){
      Serial.println("updated control data " + updated_value->toString());
    }
}
