

WiFiClient client;

template<class SENDTYPE>
class DataSender{
  public: 
  int value;
  String host;
  int port;

  DataSender(char * _host,int _port){
    value = 0;
    host = _host;
    port = _port;
  }

  void send_data(SENDTYPE data_to_send){
    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host.c_str(), port);     
    }
    
    ++value;

//    Serial.print(String("sending data ") + value + "\n");

    client.write((char*)&data_to_send, sizeof(SENDTYPE));
    unsigned long timeout = millis();

    // Read all the lines of the reply from server and print them to Serial
    while(client.available()) {
        String line = client.readStringUntil('.');
        Serial.print(line);
    }
  }

};
