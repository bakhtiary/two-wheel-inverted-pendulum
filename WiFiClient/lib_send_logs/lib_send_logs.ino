#include <WiFi.h>


const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";

#include "data_sender.h"

struct MydataStuff: public Datagram{
  
  int x;
  int y;
  MydataStuff(int x, int y): Datagram(0), x(x), y(y){}
  int get_len(){return sizeof(this);}
};

struct ControlData: public Datagram{

  int x;
  float y;
  int get_len(){return sizeof(this);}
};

DataSender dataSender("192.168.1.134", 12345);

void setup()
{
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
    dataSender.init();
}




void loop()
{
    delay(500);
    MydataStuff data_stuff{10,11};
    dataSender.send_data(data_stuff);
//    ControlData control_data;
//    if (dataSender.get_data()){
//      Serial.println(String("Got data") + control_data.x + " " + control_data.y);
//    }
}
