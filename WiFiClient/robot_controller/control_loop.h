Adafruit_MPU6050 mpu;



void control_loop( void * parameter) {
    Shared_data * shared_data = (Shared_data *) parameter;
    QueueHandle_t tx_logs_queue = shared_data->tx_logs;

  
    for(;;)
    {
      delay(100); // will pause Zero, Leonardo, etc until serial console opens
      time_t start_time = millis();

//      Serial.print("loop() task1 running on core ");
//      Serial.println(xPortGetCoreID());
    
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);

      

      time_t end_time = millis();

      Sending_data sendingdata{start_time, end_time, a, g};
      xQueueSend(tx_logs_queue, &sendingdata, portMAX_DELAY);
    }

}
