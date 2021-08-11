
String get_time(time_t start_time, unsigned long passed_millis){ 
  return String(start_time + passed_millis/1000) + String(passed_millis % 1000)+"000000";
}

String log_message(Sending_data & sending_data){
    return "more data";
}

String get_data_payload( QueueHandle_t tx_logs_queue,  time_t start_time){

    Sending_data sending_data;
    
    String PostData="{\"streams\": [";
    int max_number_of_logs = 100;
    {
      int i;
      for(i = 0; i < max_number_of_logs; i++){
        if (xQueueReceive(
          tx_logs_queue,
          &sending_data, 
          10 ) == pdPASS)
        {
          PostData = "{ \"stream\": { \"log_type\": \"control_loop\", \"run_number\": \"5\" }, \"values\": [ [ \"" +
          get_time(start_time, sending_data.control_start_time) + 
          "\", \"" + 
          log_message(sending_data)+"\"] ] }," + 
          PostData;
        }
      }
//      if (i == max_number_of_logs){
//          PostData = "{ \"stream\": { \"log_type\": \"warning\", \"run_number\": \"5\" }, \"values\": [ [ \"" +
//          get_time(start_time, millis()) + 
//          "\", \"" + 
//          "There were more logs but we stopped"+
//          "\"] ] }," + 
//          PostData;
//      }
    }
    Serial.println(PostData);
    PostData.setCharAt(PostData.lastIndexOf(','), ' ');
   
      PostData += "]} \n";
//    PostData += "{ \"stream\": { \"foo\": \"bar3\" }, \"values\": [ [ \"1628498939000000178\", \"fizzbuzz28 dfd\"] ] }]}";

    return PostData;

}

void communication_log_loop(void * parameter){
  Shared_data * shared_data = (Shared_data *) parameter;
  QueueHandle_t tx_logs_queue = shared_data->tx_logs;

  time_t start_time;
  time(&start_time);

  Serial.println(String("comm log loop() running on core ") + xPortGetCoreID());
  
  for(;;){
    String PostData = get_data_payload(tx_logs_queue, start_time);
    WiFiClient client;
    const char* host = "192.168.1.134";
    if (!client.connect(host, 3100)) {
        Serial.println("connection failed");
    }

    client.println("POST /loki/api/v1/push HTTP/1.1");
    client.println("Host:  192.168.1.134");
    client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println("Content-Type: application/json");
    client.println("Accept: */*");
    client.print("Content-Length: ");
    client.println(PostData.length());
    client.println();
    client.println(PostData);

    Serial.println("checking response.");

    unsigned long timeout = millis();
    while (client.available() == 0) {
        if (millis() - timeout > 5000) {
            Serial.println(">>> Client Timeout !");
        }
    }
    
    while(client.available()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
    }

    client.stop();
    
  }
}
