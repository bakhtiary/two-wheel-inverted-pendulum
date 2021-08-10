const char* ssid     = "MIWIFI_jTA4";
const char* password = "m4eEUQGF";

const char* host = "192.168.1.134";
const int httpPort = 5000;

int value = 0;

void communication_loop(void * parameter){
    Shared_data * shared_data = (Shared_data *) parameter;
  
    // Use WiFiClient class to create TCP connections
    WiFiClient client;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }

    for(;;){
      delay(5000);
      ++value;
  
      Serial.print("connecting to ");
      Serial.println(host);
      Serial.print("loop() running on core ");
      Serial.println(xPortGetCoreID());

      // We now create a URI for the request
      String url = "/robot_data";
  
      Serial.print("Requesting URL: ");
      Serial.println(url);
  
      // This will send the request to the server
      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                   "Host: " + host + "\r\n" +
                   "Connection: close\r\n\r\n");
      unsigned long timeout = millis();
      while (client.available() == 0) {
          if (millis() - timeout > 5000) {
              Serial.println(">>> Client Timeout !");
              client.stop();
              return;
          }
      }
  
      // Read all the lines of the reply from server and print them to Serial
      while(client.available()) {
          String line = client.readStringUntil('\r');
          Serial.print(line);
      }
  
      Serial.println();
      Serial.println("closing connection");
    }
}
