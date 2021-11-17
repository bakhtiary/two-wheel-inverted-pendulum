#include <WiFi.h>

struct CommunicationData{
  int id;
  virtual String toString();
};

class CommunicationChannel{
  String host;
  int port;
  int MAX_REGISTRY_SIZE;
  CommunicationData ** communicationDatas;
  int * communicationSizes;
  
  public: 
    WiFiClient client;

  CommunicationChannel(const char * host,const int port, int MAX_REGISTRY_SIZE):
  host(host), port(port), MAX_REGISTRY_SIZE(MAX_REGISTRY_SIZE)
  {
    communicationDatas = new CommunicationData * [MAX_REGISTRY_SIZE]();
    communicationSizes = new int [MAX_REGISTRY_SIZE]();
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
      client.write(((char*) &data_to_send) + sizeof(int), data_size-sizeof(int));/*vtable takes up 4 bytes*/
      unsigned long timeout = millis();
    }
  }

  void register_data(CommunicationData * cd, int cd_size){
    
    if (cd->id >= MAX_REGISTRY_SIZE || cd->id < 0){
      Serial.println("error cd->id >= MAX_REGISTRY_SIZE || MAX_REGISTRY_SIZE < 0.");
      Serial.println(String("id is ") + cd->id + " MAX_REGISTRY_SIZE is " + MAX_REGISTRY_SIZE );
    }
    if (communicationSizes[cd->id] != 0){ // already set
      Serial.println("error communicationSizes[cd->id] != 0");
      Serial.println(cd->id);
    }

    communicationDatas[cd->id] = cd;
    communicationSizes[cd->id] = cd_size;
  }
  CommunicationData * update_registers(){
    Serial.println("checking registers");

    if(client.available()){
      Serial.println("data is here");
      int id;
      client.readBytes((char*) &id,sizeof(int));
      
      if(id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0 || id < 0){
        Serial.println("error id >= MAX_REGISTRY_SIZE || communicationSizes[id] == 0 || id < 0");
        Serial.println(String("ID is ") + id + " MAX_REGISTRY_SIZE is " + MAX_REGISTRY_SIZE + " communicationSizes[id] is " + communicationSizes[id]);
      }
      else{
        client.readBytes((
          (char*) communicationDatas[id])+sizeof(int)*2,/*one for vtable one for id*/
          communicationSizes[id] - sizeof(int)*2  /*one for vtable one for id*/
        );
        Serial.println(String("updated id") + id );
        return communicationDatas[id];
      }
    } 
    return 0;
  }
};
