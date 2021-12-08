#include <robotics_config.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include "robot_control.pb.h"
#include "EspMQTTClient.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <lib_motor_controller.h>
#include <data_sender.h>
#define INTERRUPT_PIN 2  // use pin 2 on Arduino Uno & most boards
#include "OTA.h"
#include "MPU.h"
#include "Wire.h"
#include "pid_controller.h"
#include "neural_network_controller.h"


MPU6050 mpu;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector


EspMQTTClient client(
  ssid,
  password,
  host_ip,  // MQTT Broker server ip
  0,   // Can be omitted if not needed
  0,   // Can be omitted if not needed
  "TestClient",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);

int active_controller = RobotControl_ActivateController_ControllerType_DEACTIVATED;


void onConnectionEstablished(){
 
  client.subscribe("mytopic/liveness", [](const String & topic, const String & payload) {
    client.executeDelayed(5 * 1000, []() {
      client.publish("mytopic/liveness", String("I am alive, active controller is ") + active_controller);
    });
  });

  // Publish a message to "mytopic/test"
  client.publish("mytopic/liveness", "This is a message"); // You can activate the retain flag by setting the third parameter to true
  

  client.subscribe("activate_controller_request", [](uint8_t* payload, unsigned int message_length) {
    RobotControl_ActivateController message = RobotControl_ActivateController_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(payload, message_length);
    bool status = pb_decode(&stream, RobotControl_ActivateController_fields, &message);
    active_controller = message.type;
  }, 1);
}

void setup_motors();

void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  setup_ota();

  setup_mpu(mpu, dmpReady, mpuIntStatus, devStatus, packetSize, INTERRUPT_PIN);
  
  setup_motors();
  
}

Control_Data control_data{650.0, 5.0, 600.0, 140.0, 0, 0};

Motor motor1 = Motor(25,33,32,1,20);
Motor motor2 = Motor(26,27,14,2,20);

Pid_Controller pid_controller(control_data, motor1, motor2);


NN_Controller nn_controller(motor1, motor2);

void setup_motors(){
  motor1.enable();
  motor2.enable();
}

int loop_number = 0;

void loop() {
  ArduinoOTA.handle();
  client.loop();

  if(loop_number == 0){
    motor1.low_power_offset = control_data.minimal_motor_power;
    motor2.low_power_offset = control_data.minimal_motor_power;
  }
  
  loop_number += 1;
  time_t start_time = millis();

  if (!dmpReady) return;


  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet

      // display Euler angles in degrees
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
      if (active_controller == RobotControl_ActivateController_ControllerType_PID){
        pid_controller.control(ypr[1]);
      }else if (active_controller == RobotControl_ActivateController_ControllerType_NEURAL_NET){
        nn_controller.control(ypr);
      }
//      client.publish("robot_status/running_PID_control", String(" active controller: ") + active_controller + " " + power + " loop_number " + loop_number );


      time_t current_time = millis();    


  }

  
}
