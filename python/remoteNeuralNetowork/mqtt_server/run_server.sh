docker rm mosquitto
docker run -it --name mosquitto -p 1883:1883 -v $(pwd)/mosquitto:/mosquitto/ eclipse-mosquitto 
#docker run -it -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto.conf -v ./mosquito_data:/mosquitto/data -v ./mosquitto_log:/mosquitto/log eclipse-mosquitto
