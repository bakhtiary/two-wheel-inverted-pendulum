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
 
  client.subscribe("robot_status/liveness", [](const String & topic, const String & payload) {
    client.executeDelayed(5 * 1000, []() {
      client.publish("robot_status/liveness", String("I am alive, active controller is ") + active_controller);
    });
  });

  // Publish a message to "mytopic/test"
  client.publish("robot_status/liveness", "This is a message"); // You can activate the retain flag by setting the third parameter to true
  

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
  Serial.println("setting up mpu");

  setup_mpu(mpu, dmpReady, mpuIntStatus, devStatus, packetSize, INTERRUPT_PIN);
  Serial.println("skipping setting up mpu - setting up motors");

  setup_motors();
  
}

Control_Data control_data{650.0, 5.0, 600.0, 140.0, 0, 0};

Motor motor1 = Motor(25,33,32,1,20);
Motor motor2 = Motor(26,27,14,2,20);

Pid_Controller pid_controller(control_data, motor1, motor2, client);


NN_Controller nn_controller(motor1, motor2);

void setup_motors(){
  motor1.enable();
  motor2.enable();
}

int loop_number = 0;
int loop_count_since_dmp_ready = 0;
void loop() {
  ArduinoOTA.handle();
  client.loop();
  printf("looping \n ");
  if(loop_number == 0){
    motor1.low_power_offset = control_data.minimal_motor_power;
    motor2.low_power_offset = control_data.minimal_motor_power;
  }
  
  loop_number += 1;
  time_t start_time = millis();

  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet

      if (loop_count_since_dmp_ready == 0){
        client.publish("robot_status/warning", "we did not do extra loops before reading the next packet. The cpu can not handle this + loop number is " + String(loop_number));
      }
      loop_count_since_dmp_ready = 0;


      // display Euler angles in degrees
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
      if (active_controller == RobotControl_ActivateController_ControllerType_PID){
        pid_controller.control(ypr[1]);
      }else if (active_controller == RobotControl_ActivateController_ControllerType_NEURAL_NET){
        nn_controller.control(ypr,0,0);
      }
//      client.publish("robot_status/running_PID_control", String(" active controller: ") + active_controller + " " + power + " loop_number " + loop_number );

      time_t current_time = millis();    

  } else {
    loop_count_since_dmp_ready += 1;
  }
  
}
