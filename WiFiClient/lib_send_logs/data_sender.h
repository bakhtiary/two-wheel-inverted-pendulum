#include <WiFi.h>

struct Datagram{
  int id;
  virtual int get_len();
  Datagram(int id):id(id){}
};


class DataSender{
  public: 
  WiFiClient client;
  int value;
  String host;
  int port;
  bool first_connection_succeeded;

  DataSender(const char * _host,const int _port){
    value = 0;
    host = _host;
    port = _port;
  }

  void init(){
    client.connect(host.c_str(), port);
    if (client.connected()){
      first_connection_succeeded = true;
    }else{
      first_connection_succeeded = false;
    }

  }

  void send_data(Datagram & data_to_send){
    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host.c_str(), port);     
    } else {
      client.write((char*) &data_to_send, data_to_send.get_len());
      unsigned long timeout = millis();
    }
  }

  bool get_data(){
    if(client.available()) {
//      client.readBytes((char*) &data_to_recieve,sizeof(RECIEVE_TYPE));
      return true;
    }
    else{
      return false;
    }
  }
};
