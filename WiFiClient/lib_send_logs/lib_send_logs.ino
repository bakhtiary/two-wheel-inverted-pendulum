/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <WiFi.h>


const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";


// Use WiFiClient class to create TCP connections
#include "data_sender.h"

void setup()
{
    Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
char* host = "192.168.1.134";
int httpPort = 12345;

class MydataStuff{
public:
  int x;
  int y;
};

DataSender <MydataStuff> dataSender(host,httpPort);

void loop()
{
    MydataStuff data_stuff{10,11};
    dataSender.send_data(data_stuff);
}
