#include <WiFi.h>


template<class SEND_TYPE, class RECIEVE_TYPE>
class DataSender{
  public: 
  WiFiClient client;
  int value;
  String host;
  int port;

  DataSender(const char * _host,const int _port){
    value = 0;
    host = _host;
    port = _port;
  }

  void send_data(SEND_TYPE data_to_send){
    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host.c_str(), port);     
    } else {
      client.write((char*) &data_to_send, sizeof(SEND_TYPE));
      unsigned long timeout = millis();
    }
  }

  int get_data(RECIEVE_TYPE & data_to_recieve){
    if(client.available()) {
      client.readBytes((char*) &data_to_recieve,sizeof(RECIEVE_TYPE));
      return true;
    }
    else{
      return false;
    }
  }
};
