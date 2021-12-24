#include <robotics_config.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include "robot_control.pb.h"
#include "EspMQTTClient.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <lib_motor_controller.h>
#define INTERRUPT_PIN 2  // use pin 2 on Arduino Uno & most boards
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

class WeightParamsUpdater{
  const int weight_params_count;
  const Params ** weight_params ;
  public:
  WeightParamsUpdater(const int weight_params_count, const Params ** weight_params):
  weight_params_count(weight_params_count), weight_params(weight_params) {}
  void from_request(RobotControl_ModelUpdateRequest & requestMessage){
    int id = requestMessage.param_id;
    Serial.println(String("updating " )+ id + " from location " + requestMessage.param_start_offset + " with len " + requestMessage.param_values.values_count);
    for(int i = 0; i < weight_params_count; i++){
      if(id == weight_params[i]->class_id){
        for(int j = 0, k = requestMessage.param_start_offset; j < requestMessage.param_values.values_count && k < weight_params[i]->len; j++, k++){
          weight_params[i]->values[k] = requestMessage.param_values.values[j];
        }    
      }
    }
  }
};

const Params * weight_params[] = {&mu_0_weight_params,&mu_0_bias_params,&mu_2_weight_params,&mu_2_bias_params, &mu_4_weight_params, &mu_4_bias_params};
WeightParamsUpdater params_updater(NUM(weight_params),weight_params);

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
int run_id = 0;
int loop_number = 0;
float lpower = 0, rpower = 0;

void onConnectionEstablished(){  

  client.subscribe("robot/activate_controller_request", [](uint8_t* payload, unsigned int message_length) {
    RobotControl_ActivateController message = RobotControl_ActivateController_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(payload, message_length);
    bool status = pb_decode(&stream, RobotControl_ActivateController_fields, &message);
    active_controller = message.type;
    run_id = message.run_id;
    lpower = rpower = 0;
    loop_number = 0;
  }, 1);

  client.subscribe("robot/model_update_request", [](uint8_t* payload, unsigned int message_length) {
    RobotControl_ModelUpdateRequest message = RobotControl_ModelUpdateRequest_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(payload, message_length);
    bool status = pb_decode(&stream, RobotControl_ModelUpdateRequest_fields, &message);
//    params_updater.from_request(message);
  }, 1);

  client.subscribe("robot/model_params_review_request", [](uint8_t* payload, unsigned int message_length) {
      client.publish("robot/model_params_review_response", nn.toString());
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

  Serial.println("setting up mpu");

  setup_mpu(mpu, dmpReady, mpuIntStatus, devStatus, packetSize, INTERRUPT_PIN);
  Serial.println("skipping setting up mpu - setting up motors");

  setup_motors();
  
}

Control_Data control_data{650.0, 5.0, 600.0, 140.0, 0, 0};

Motor motor1 = Motor(25,33,32,1,20);
Motor motor2 = Motor(26,27,14,2,20);

Pid_Controller pid_controller(control_data, client);


NN_Controller nn_controller(client);

void setup_motors(){
  motor1.enable();
  motor2.enable();
}

int loop_count_since_dmp_ready = 0;
void loop() {
  Serial.println("looping" );
  if(loop_number == 0){
    motor1.low_power_offset = control_data.minimal_motor_power;
    motor2.low_power_offset = control_data.minimal_motor_power;
  }
  
  time_t start_time = millis();

  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet

      if (loop_count_since_dmp_ready == 0){
        client.publish("robot/warning", "we did not do extra loops before reading the next packet. The cpu can not handle this + loop number is " + String(loop_number));
      }
      loop_count_since_dmp_ready = 0;

      // display Euler angles in degrees
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
      if (active_controller == RobotControl_ActivateController_ControllerType_PID){
        lpower = rpower = pid_controller.control(ypr[1]);
      }else if (active_controller == RobotControl_ActivateController_ControllerType_NEURAL_NET){
        TransferValues * result = nn_controller.control(ypr, 0, 0);
        float max_motor_power = 500;
        lpower = result->values[0]*max_motor_power;
        rpower = result->values[1]*max_motor_power;
      }
      motor1.setPower(lpower);
      motor2.setPower(rpower);
      float reward = 1 - fabs(ypr[1]) - (fabs(lpower) + fabs(rpower))/1000.0;

      String reward_string = isnan(reward)?"NaN":String(reward);

//      String inputs_json = inputs.toJson() ;
      String inputs_json = inputs.toJson() + ", \"output_values\": " + ta.output->toJson();

      Serial.println("sending data" );
      Serial.println(inputs.toJson());
      
      client.publish("robot/reward", inputs_json);

      loop_number += 1;

//      client.publish("robot_status/running_PID_control", String(" active controller: ") + active_controller + " " + power + " loop_number " + loop_number );
      time_t current_time = millis();
  } else {
    loop_count_since_dmp_ready += 1;
  }
  
}
