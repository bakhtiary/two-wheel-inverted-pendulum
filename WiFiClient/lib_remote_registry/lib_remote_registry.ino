#include "robotics_config.h"
#include "remote_registry.h"
#include "remote_registry_data.h"

struct SendingData3{
  int a2;
  int b2;
};

CommunicationChannel<10> communication_channel{host_ip, host_port};

Data1 * data1;
Data2 * data2;
bool first_connection_succeeded;
void setup() {


    Serial.begin(115200);
    delay(10);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    } 

    Serial.print("WiFi connected. ");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    data1 = new Data1();
    data2 = new Data2();
    first_connection_succeeded = communication_channel.init();
    Serial.println(first_connection_succeeded);

    communication_channel.register_data(data1, sizeof(Data1));
    communication_channel.register_data(data2, sizeof(Data2));
    
}

void loop() {
  TimeData timedata(3,millis());
  communication_channel.send_data(timedata,sizeof(timedata));
  communication_channel.update_registers();
  Serial.println(data1->toString());
  delay(500);
}
