#include <WiFi.h>

class HostAndPort{
  public:
  String host;
  int port;
  HostAndPort(const char * host, int port){
    this->host = host;
    this->port = port;
  }  
};

void TaskBlink(void *pvParameters)  // This is a task.
{
  HostAndPort * host_and_port = (HostAndPort *) pvParameters;

  WiFiClient client;

  for (;;) // A Task shall never return or exit.
  {
    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host_and_port->host.c_str(), host_and_port->port);     
    }else{
      delay(1);
    }
  }
}

template<class SEND_TYPE, class RECIEVE_TYPE>
class DataSender{
  public: 
  WiFiClient client;
  int value;

  DataSender(HostAndPort * host_and_port){
    value = 0;

//    xTaskCreatePinnedToCore(TaskBlink
//    ,  "TaskBlink"   // A name just for humans
//    ,  1024  // This stack size can be checked & adjusted by reading the Stack Highwater
//    ,  host_and_port
//    ,  0  // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
//    ,  NULL 
//    ,  ARDUINO_RUNNING_CORE);
    }

  void send_data(SEND_TYPE data_to_send){
    if (client.connected()){
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
