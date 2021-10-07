#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"


// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

#include <lib_motor_controller.h>
#include <data_sender.h>
#include "communication_structures.h"

Control_data control_data{650.0, 5.0, 600.0, 140.0, 0, 0};

Motor motor1 = Motor(25,33,32,1,20);
Motor motor2 = Motor(26,27,14,2,20);

MPU6050 mpu;
#define OUTPUT_READABLE_YAWPITCHROLL

#define INTERRUPT_PIN 2  // use pin 2 on Arduino Uno & most boards
#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;

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

// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

DataSender <Sending_data, Control_data> * sender;
// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================
const char* host = "192.168.1.134";
const int httpPort = 12345;
const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";

void setup() {

    Serial.println(String("connecting to wifi: ")+ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (115200 chosen because it is required for Teapot Demo output, but it's
    // really up to you depending on your project)
    Serial.begin(115200);
    while (!Serial); // wait for Leonardo enumeration, others continue immediately

    // initialize device
    Serial.println(F("Initializing I2C devices..."));
    mpu.initialize();
    pinMode(INTERRUPT_PIN, INPUT);

    // verify connection
    Serial.println(F("Testing device connections..."));
    Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

    // load and configure the DMP
    Serial.println(F("Initializing DMP..."));
    devStatus = mpu.dmpInitialize();

    Serial.println(F("setting offsets..."));

    // supply your own gyro offsets here, scaled for min sensitivity
    mpu.setXGyroOffset(7);
    mpu.setYGyroOffset(13);
    mpu.setZGyroOffset(126);
    mpu.setZAccelOffset(1688); // 1688 factory default for my test chip

    Serial.println(F("checking devstatus..."));

    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // Calibration Time: generate offsets and calibrate our MPU6050
        mpu.CalibrateAccel(6);
        mpu.CalibrateGyro(6);
        mpu.PrintActiveOffsets();
        // turn on the DMP, now that it's ready
        Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        // enable Arduino interrupt detection
        Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
        Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
        Serial.println(F(")..."));
        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        Serial.print(F("DMP Initialization failed (code "));
        Serial.print(devStatus);
        Serial.println(F(")"));
    }

    // configure LED for output
    pinMode(LED_PIN, OUTPUT);

    motor1.enable();
    motor2.enable();
   
    sender = new DataSender <Sending_data, Control_data> (host,httpPort);
}

float previous_error = 0 ,commulative_error = 0;

// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

int loop_number = 0;

void loop() {
//    Serial.println(F("starting loop"));

    if(loop_number == 0){
      motor1.low_power_offset = control_data.minimal_motor_power;
      motor2.low_power_offset = control_data.minimal_motor_power;
    }
    
    loop_number += 1;
    time_t start_time = millis();

    // if programming failed, don't try to do anything
    if (!dmpReady) return;
    // read a packet from FIFO
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet

 
        // display Euler angles in degrees
        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
        float error = ypr[1] + control_data.offset;
        float delta_error = error - previous_error;
        commulative_error *= 0.99;
        commulative_error += error;
      
        float power = error*control_data.proportional + commulative_error*control_data.integration + delta_error*control_data.derivative;

        Serial.print("ypr[0]\t");
        Serial.print(ypr[0]);
        Serial.print("ypr[1]\t");
        Serial.print(ypr[1]);
        Serial.print("ypr[2]\t");
        Serial.print(ypr[2]);
        Serial.print("\t");
        Serial.print(power);
        Serial.print("\t");
        Serial.print(error);
        Serial.print("\t");
        Serial.print(delta_error);
        Serial.print("\t");
        Serial.print(commulative_error);
        Serial.println(".");


        motor1.setPower(power);
        motor2.setPower(power);

        time_t current_time = millis();

        previous_error = error;

        handle_server_communication(loop_number, start_time, current_time, power);        
    }   
}

void handle_server_communication(int & loop_number,time_t & start_time,time_t & current_time,float & power){
    if (!sender->first_connection_succeeded)
      return;
    Sending_data sendingdata{loop_number, start_time, current_time, power};
    sender->send_data(sendingdata);  

    if (sender->get_data(control_data)){
      Serial.println("updated control data " + control_data.get_string());
      loop_number = 0;
    }
}
