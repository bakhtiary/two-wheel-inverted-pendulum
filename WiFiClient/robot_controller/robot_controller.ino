
#include <WiFi.h>
#include <data_sender.h>
#include <Adafruit_MPU6050.h>
#include <Wire.h>
#include <lib_motor_controller.h>


const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";
char* host = "192.168.1.134";
int httpPort = 12345;
Adafruit_MPU6050 mpu;

#include "communication.h"

DataSender <Sending_data, Control_data> sender(host,httpPort);

Motor motor1 = Motor(26,27,25,1,120);
Motor motor2 = Motor(12,14,13,2,120);

void setup()
{
    Serial.begin(115200);
    while (!Serial)
      delay(10); // will pause Zero, Leonardo, etc until serial console opens
    
    if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
      while (1) {
        delay(10);
      }
    }

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
    Serial.println("WiFi connecteds2");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP()); 

    motor1.enable();
    motor2.enable();
}

unsigned long loop_number = 0;
Control_data control_data{0, 0, 1000};
void loop()
{
    loop_number += 1;
    time_t start_time = millis();
  
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    time_t end_time = millis();

    sensors_vec_t & acc = a.acceleration;
    sensors_vec_t & gyro = g.gyro;
        

    int power = (acc.y - control_data.offset) * control_data.proportional;

    motor1.setPower(power);
    motor2.setPower(power);
    
    Sending_data sendingdata{loop_number,start_time, end_time, acc.x, acc.y, acc.z, gyro.x, gyro.y, gyro.z};
    sender.send_data(sendingdata);      

    if (sender.get_data(control_data)){
      Serial.println("updated control data " + control_data.get_string());
    }
       
    delay(control_data.delay_time);
}
