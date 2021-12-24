#include <robotics_config.h>
#include "mqtt.h"
#include "mpu.h"

/*
  SimpleMQTTClient.ino
  The purpose of this exemple is to illustrate a simple handling of MQTT and Wifi connection.
  Once it connects successfully to a Wifi network and a MQTT broker, it subscribe to a topic and send a message to it.
  It will also send a message delayed 5 seconds later.
*/


void setup()
{
  Serial.begin(115200);
  mpu_setup();
  mqttClientSetup();
}


void loop()
{
    mqttclient.loop();

    mpu_read();
}
