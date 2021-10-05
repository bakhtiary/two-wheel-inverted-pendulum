#include <WiFi.h>

#include "remote_registry.h"

#define MAX_REGISTRY_SIZE 10

class CommunicationChannel{
  String host;
  int port;
  bool first_connection_succeeded;
  CommunicationData * communicationDatas[MAX_REGISTRY_SIZE];
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

  void register_data(CommunicationData * cd, int cd_size){
    
    if (cd->id > MAX_REGISTRY_SIZE){
      Serial.println("error cd->id > MAX_REGISTRY_SIZE");
    }
    if (communicationSizes[cd->id] == 0){
      Serial.println("error communicationSizes[cd->id] == 0");
    }

    communicationDatas[cd->id] = cd;
    communicationSizes[cd->id] = cd_size;
  }
  bool update_registers(){
    if(client.available()){
      int id;
      client.readBytes((char*) &id,sizeof(int));
      
      if(id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0 ){
        Serial.println("error id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0");
      }
      else{
        client.readBytes(((char*) communicationDatas[id])+sizeof(int),communicationSizes[id]-sizeof(int));
        Serial.println(String("updated id") + id );
        return true;
      }
    } 
    return false;
  }
};

struct SendingData3{
  int a2;
  int b2;
};

CommunicationChannel * communication_channel;


//const char* ssid     = "MIWIFI_jTA4";
//const char* password = "m4eEUQGF";

const char* ssid     = "not_available_2g";
const char* password = "ThePasswordIsGreenHorseCamelCaseNoSpaces";
Data1 * data1;
Data2 * data2;


void setup() {


    Serial.begin(115200);
    delay(10);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.print("WiFi connected. ");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    data1 = new Data1();
    data2 = new Data2();

    communication_channel = new CommunicationChannel("192.168.1.110", 12345);
    communication_channel->register_data(data1, sizeof(Data1));
    communication_channel->register_data(data2, sizeof(Data2));
    
}

void loop() {
  TimeData timedata(3,millis());
  communication_channel->send_data(timedata,sizeof(timedata));
  communication_channel->update_registers();
  Serial.println(data1->toString());
  delay(500);
}
