#include <robotics_config.h>
#include <ArduinoJson.h>

#include "mqtt.h"
#include "mpu.h"
#include "motors.h"
#include "pid_controller.h"
#include "neural_controller.h"

Pid_Controller pid_controller;
Neural_Controller neural_controller;

enum Controller_Type{
    NONE, PID, NEURAL_NET, TIMED_MOVE
} active_controller;

int run_id = 0;
int loop_number = 0;

int timed_move_rpower = 0;
int timed_move_lpower = 0;
unsigned long timed_move_end = 0;

void setController(const String & requestMessage){
  DynamicJsonDocument doc(256);
  deserializeJson(doc, requestMessage);

  run_id = doc["run_id"]; 
  String controller_type = doc["controller_type"];

  loop_number = 0;
  if(controller_type.equals("PID")){
    active_controller = PID;
  }else if(controller_type.equals("NEURAL_NET")){
    active_controller = NEURAL_NET;
  }else if(controller_type.equals("TIMED_MOVE")){
    active_controller = TIMED_MOVE;
    timed_move_rpower = doc["lpower"];
    timed_move_lpower = doc["rpower"];
    timed_move_end = doc["move_millis"];
    timed_move_end += millis();
  }
  else{
    active_controller = NONE;
  }
}


void setup()
{
  Serial.begin(115200);
  mpu_setup();
  mqttClientSetup();
  setupMotors();
}


void loop()
{
    mqttclient.loop();
    Quaternion q; float ypr[3];float mpu_read_done = mpu_read(q,ypr);
    if (!mpu_read_done){
      return ;
    }
    float rpower, lpower;
    if (active_controller == PID){
      lpower = rpower = pid_controller.control(ypr[1]);
    }else if(active_controller == NEURAL_NET){
      neural_controller.control(lpower, rpower, ypr, 0, 0);
    }else if(active_controller == TIMED_MOVE){
      lpower = timed_move_lpower;
      rpower = timed_move_rpower;
      moveMotors(lpower, rpower);
      if (millis() >= timed_move_end){
        active_controller = NONE;
      }
    }
    else {
      lpower = rpower = 0;
    }

    moveMotors(lpower, rpower);

    float reward = 1 - fabs(ypr[1]) - (fabs(lpower) + fabs(rpower))/100.0;
    StaticJsonDocument<300> doc;
    doc["reward"] = reward;
    doc["run_id"] = run_id;
    doc["loop_number"] = loop_number; loop_number += 1;
    doc["output_values"][0] = ta.output->values[0];
    doc["output_values"][1] = ta.output->values[1];
    doc["input_values"][0] = inputs.values[0];
    doc["input_values"][1] = inputs.values[1];
    doc["input_values"][2] = inputs.values[2];
//    doc["left_motor_power"] = lpower;
//    doc["right_motor_power"] = rpower;
//    doc["active_controller"] = active_controller;
//    doc["millis_since_restart"] = millis();

    String message_buffer;
    serializeJson(doc, message_buffer);
    mqttclient.publish("robot/alive", message_buffer); 

}

void onConnectionEstablished()
{
  // Subscribe to "mytopic/test" and display received message to Serial
  mqttclient.subscribe("robot/set_controller", [](const String & payload) {
    setController(payload);    
  });

  mqttclient.subscribe("robot/update_weights", [](const String & payload) {
    params_updater.from_request(payload);
  });

  mqttclient.subscribe("robot/debug/nn", [](const String & payload) {
    mqttclient.publish("robot/debug/nn_fc1", fc1.toString() ); 
    mqttclient.publish("robot/debug/nn_relu1", relu1.toString() ); 
    mqttclient.publish("robot/debug/nn_fc2_weights", fc2.weights.toString() ); 
    mqttclient.publish("robot/debug/nn_fc2_biases", fc2.biases.toString() ); 
    mqttclient.publish("robot/debug/nn_fc2_output", fc2.output->toString() ); 
    mqttclient.publish("robot/debug/nn_relu2", relu2.toString() ); 
    mqttclient.publish("robot/debug/nn_fc3", fc3.toString() ); 
    mqttclient.publish("robot/debug/nn_ta", ta.toString() ); 

  });


}
