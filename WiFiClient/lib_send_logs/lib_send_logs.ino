#include <WiFi.h>


const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";

#include "data_sender.h"

void setup()
{
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

class MydataStuff{
public:
  int x;
  int y;
};

class ControlData{
public:
  int x;
  float y;
};

HostAndPort host_and_port("192.168.1.134",12345);
DataSender <MydataStuff,ControlData> dataSender(&host_and_port);

void loop()
{
    delay(500); 
    MydataStuff data_stuff{10,11};
    dataSender.send_data(data_stuff);
    ControlData control_data;
    if (dataSender.get_data(control_data)){
      Serial.println(String("Got data") + control_data.x + " " + control_data.y);
    }
}
