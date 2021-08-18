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

const char* host = "192.168.1.134";
const int httpPort = 12345;

// Use WiFiClient class to create TCP connections
WiFiClient client;


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
    if (!client.connect(host, httpPort)) {
      Serial.println("connection failed");
    }
}

int value = 0;

void loop()
{
    ++value;

//    Serial.print(String("sending data ") + value + "\n");

    client.print(String("some data\n") + value);
    unsigned long timeout = millis();

    if (!client.connected()){
        Serial.println(">>> client disconnected !");
        client.stop();
        client.connect(host, httpPort);     
    }

    // Read all the lines of the reply from server and print them to Serial
    while(client.available()) {
        String line = client.readStringUntil('.');
        Serial.print(line);
    }

}
