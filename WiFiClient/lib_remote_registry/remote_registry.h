#include <WiFi.h>

struct CommunicationData{
  int id;
  virtual String toString();
};

template <int MAX_REGISTRY_SIZE>
class CommunicationChannel{
  String host;
  int port;
  CommunicationData * communicationDatas[MAX_REGISTRY_SIZE];
  int communicationSizes[MAX_REGISTRY_SIZE];
  
  public: 
    WiFiClient client;

  CommunicationChannel(const char * _host,const int _port){
    host = _host;
    port = _port;
  }

  bool init(){
    client.connect(host.c_str(), port);
    return client.connected();
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
  CommunicationData * update_registers(){
    if(client.available()){
      int id;
      client.readBytes((char*) &id,sizeof(int));
      
      if(id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0 ){
        Serial.println("error id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0");
      }
      else{
        client.readBytes(((char*) communicationDatas[id])+sizeof(int),communicationSizes[id]-sizeof(int));
        Serial.println(String("updated id") + id );
        return communicationDatas[id];
      }
    } 
    return 0;
  }
};
