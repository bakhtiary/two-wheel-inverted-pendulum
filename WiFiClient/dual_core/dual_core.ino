void setup() {
  Serial.begin(115200);
  Serial.print("setup() running on core ");
  Serial.println(xPortGetCoreID());

  TaskHandle_t Task1;
  xTaskCreatePinnedToCore(
      Task1code, /* Function to implement the task */
      "Task1", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      0,  /* Priority of the task */
      &Task1,  /* Task handle. */
      0); /* Core where the task should run */

  TaskHandle_t Task2;
  xTaskCreatePinnedToCore(
      Task2code, /* Function to implement the task */
      "Task2", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      0,  /* Priority of the task */
      &Task2,  /* Task handle. */
      1); /* Core where the task should run */

}

void loop() {
  Serial.print("loop() running on core ");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");
  Serial.println("*********");

  Serial.println(xPortGetCoreID());
  delay(1000);
}


void Task1code( void * parameter) {
    for(;;)
    {
      Serial.print("loop() task1 running on core ");
      Serial.println(xPortGetCoreID());
    }
}



void Task2code( void * parameter) {
    for(;;)
    {
  
      Serial.print("loop() task2 running on core ");
      Serial.println(xPortGetCoreID());
    }
}
