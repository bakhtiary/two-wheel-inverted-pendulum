#include <WiFi.h>

class CommunicationData{
};

#define MAX_REGISTRY_SIZE 10

class CommunicationChannel{
  String host;
  int port;
  bool first_connection_succeeded;
  int communicationDatas[MAX_REGISTRY_SIZE];
  int communicationSizes[MAX_REGISTRY_SIZE];
  
  public: 
    WiFiClient client;

  CommunicationChannel(const char * _host,const int _port){
    host = _host;
    port = _port;
    
    client.connect(host.c_str(), port);
    if (client.connected()){
      first_connection_succeeded = true;
    }else{
      first_connection_succeeded = false;
    }
  }
  
  void send_data(const CommunicationData & data_to_send, int data_size){
    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host.c_str(), port);     
    } else {
      client.write((char*) & data_to_send, data_size);
      unsigned long timeout = millis();
    }
  }

  void register_data(CommunicationData * cd, cd_size){
    if (cd->id > MAX_REGISTRY_SIZE){
      Serial.println("error cd->id > MAX_REGISTRY_SIZE");
    }
    if (communicationSizes[cd->id != 0){
      Serial.println("error communicationSizes[cd->id != 0");
    }
    communicationDatas[cd->id] = cd;
    communicationSizes[cd->id] = cd_size;
  }
};



struct SendingData3{
  int a2;
  int b2;
};

Data1 d;
Data2 d2;

CommunicationChannel communication_channel("192.168.1.134", 12345);
communication_channel.register_data(d);
communication_channel.register_data(d2);


const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";


void setup() {
  // put your setup code here, to run once:
   Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.print("WiFi connected. ");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

}
