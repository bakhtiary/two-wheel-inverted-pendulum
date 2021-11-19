#include <robotics_config.h>
#include "remote_registry.h"
#include "remote_registry_data.h"

struct SendingData3{
  int a2;
  int b2;
};

CommunicationChannel communication_channel{host_ip, host_port, 10};

Data1 * data1;
Data2 * data2;
VarData<10> * data3;
bool first_connection_succeeded;
void setup() {


    Serial.begin(115200);
    delay(10);
    Serial.println(ssid);
    
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
    data3 = new VarData<10>();
    first_connection_succeeded = communication_channel.init();
    Serial.println(first_connection_succeeded);

    communication_channel.register_data(data1, sizeof(Data1));
    communication_channel.register_data(data2, sizeof(Data2));
    communication_channel.register_data(data3, sizeof(data3));
}

void loop() {
  TimeData timedata(3,millis());
  communication_channel.send_data(timedata,sizeof(timedata));
  CommunicationData * register_updated = communication_channel.update_registers();
  if(register_updated != 0){
    Serial.println(register_updated->toString());
  }
  delay(500);
}
