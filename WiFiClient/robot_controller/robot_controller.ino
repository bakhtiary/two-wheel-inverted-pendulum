

#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

struct Shared_data{
  QueueHandle_t tx_logs, rx_robot_parameters;
};
#include "sending_data.h"
#include "control_loop.h"
#include "communication_loop.h"
#include "communication_report_log_loop.h"

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

    configTime(0, 0, "pool.ntp.org");

    tm timeinfo;
    if(!getLocalTime(&timeinfo)){
      Serial.println("Failed to setup time");
      Serial.println("Failed to setup time");
      Serial.println("Failed to setup time");
      return;
    }
  
    QueueHandle_t tx_log_queue = xQueueCreate( 5, sizeof( Sending_data ) );
    QueueHandle_t rx_robot_parameters_queue = xQueueCreate( 5, sizeof(Sending_data));
    TaskHandle_t Task1;
    TaskHandle_t Task2;
    TaskHandle_t communication_log_task;
    Shared_data * shared_data = new Shared_data{tx_log_queue , rx_robot_parameters_queue};
    xTaskCreatePinnedToCore(
      control_loop, /* Function to implement the task */
      "control_loop", /* Name of the task */
      10000,  /* Stack size in words */
      shared_data,  /* Task input parameter */
      0,  /* Priority of the task */
      &Task1,  /* Task handle. */
      1); /* Core where the task should run */

    xTaskCreatePinnedToCore(
      communication_log_loop, /* Function to implement the task */
      "communication_log_loop", /* Name of the task */
      10000,  /* Stack size in words */
      shared_data,  /* Task input parameter */
      0,  /* Priority of the task */
      &communication_log_task,  /* Task handle. */
      0); /* Core where the task should run */
  
    
//    xTaskCreatePinnedToCore(
//      communication_loop, /* Function to implement the task */
//      "communication_loop", /* Name of the task */
//      10000,  /* Stack size in words */
//      &shared_data,  /* Task input parameter */
//      0,  /* Priority of the task */
//      &Task1,  /* Task handle. */
//      0); /* Core where the task should run */
}



void loop()
{
  Serial.print("MAIN loop() is alive and running on core ");
  Serial.println(xPortGetCoreID());
  delay(10000);
}
