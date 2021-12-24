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

void onConnectionEstablished()
{
  // Subscribe to "mytopic/test" and display received message to Serial
  mqttclient.subscribe("mytopic/test", [](const String & payload) {
    Serial.println(payload);
  });

  // Subscribe to "mytopic/wildcardtest/#" and display received message to Serial
  mqttclient.subscribe("mytopic/wildcardtest/#", [](const String & topic, const String & payload) {
    Serial.println("(From wildcard) topic: " + topic + ", payload: " + payload);
  });

  // Publish a message to "mytopic/test"
  mqttclient.publish("mytopic/test", "This is a message"); // You can activate the retain flag by setting the third parameter to true

  // Execute delayed instructions
  mqttclient.executeDelayed(5 * 1000, []() {
    mqttclient.publish("mytopic/wildcardtest/test123", "This is a message sent 5 seconds later");
  });
}
