#include "EspMQTTClient.h"

EspMQTTClient mqttclient(
  ssid,
  password,
  host_ip,  // MQTT Broker server ip
  "barebones_robot",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);


void mqttClientSetup(){
  // Optional functionalities of EspMQTTClient
  mqttclient.enableDebuggingMessages(); // Enable debugging messages sent to serial output
  mqttclient.enableHTTPWebUpdater(); // Enable the web updater. User and password default to values of MQTTUsername and MQTTPassword. These can be overridded with enableHTTPWebUpdater("user", "password").
  mqttclient.enableOTA(); // Enable OTA (Over The Air) updates. Password defaults to MQTTPassword. Port is the default OTA port. Can be overridden with enableOTA("password", port).
  mqttclient.enableLastWillMessage("TestClient/lastwill", "I am going offline");  // You can activate the retain flag by setting the third parameter to true
}
