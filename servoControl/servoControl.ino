#include <ESP8266WiFi.h>
#include <Servo.h>
#include <TimeLib.h>

// Define the pins for the servos
const int servo1Pin = D1; // Servo1 pin
const int servo2Pin = D2; // Servo2 pin
const int servo3Pin = D6; // Servo3 pin
const int servo4Pin = D7; // Servo4 pin

Servo servo1; // Declare servo1 object
Servo servo2; // Declare servo2 object
Servo servo3; // Declare servo3 object
Servo servo4; // Declare servo4 object

// WiFi credentials
const char* ssid = "Zave Mesh_Guest";
const char* password = "Zaveguestwifi1@";

// Your Node.js server settings
const char* serverHost = "192.168.1.6";
const int serverPort = 3000; // HTTP port

// Variable to store growth stage
String growth_stage;

void connectToWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void getCurrentGrowthStage() {
  WiFiClient client;

  String url = "http://" + String(serverHost) + ":" + String(serverPort) + "/growth-stage";

  if (client.connect(serverHost, serverPort)) {
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + serverHost + "\r\n" +
                 "Connection: close\r\n\r\n");

    while (client.connected()) {
      String line = client.readStringUntil('\n');

      // Check for the blank line that indicates the end of the headers
      if (line == "\r") {
        // The next line will be the growth stage
        growth_stage = client.readStringUntil('\n');
        Serial.println("Growth Stage: " + growth_stage);
        break;
      }
    }
  } else {
    Serial.println("Failed to connect to the server");
  }

  client.stop();
}

bool initialActionDone = false; // Variable to track if the initial action at 8 am has occurred

void controlServos() {

    // Perform the initial action at 8 am
    servo1.write(0); // Set servo1 to 0
    servo1.write(90); // Set servo1 to 90 degrees
    delay(45000);
    servo1.write(0); // Set servo1 to 0

    // Mark the initial action as done
    initialActionDone = true;

    // Print a reminder of the currently running servo
    Serial.println("Servo 1 is running. Watering");

    // Check the growth stage and control servos accordingly
    if (growth_stage.indexOf("Sapling") != -1) {
      servo2.write(0); // Set servo2 to 0 degrees
      servo2.write(90); // Set servo2 to 90 degrees
      delay(45000);
      servo2.write(0); // Set servo2 to 0 degrees
      
      // Print a reminder of the currently running servo
      Serial.println("Servo 2 is running. Sapling Stage");
    }

    if (growth_stage.indexOf("Flowering") != -1) {
      servo3.write(0); // Set servo3 to 0 degrees
      servo3.write(90); // Set servo3 to 90 degrees
      delay(80000);
      servo3.write(0); // Set servo3 to 0 degrees
      
      // Print a reminder of the currently running servo
      Serial.println("Servo 3 is running. Flowering Stage");
    }

    if (growth_stage.indexOf("Fruit") != -1) {
      servo4.write(0); // Set servo4 to 0 degrees
      servo4.write(90); // Set servo4 to 90 degrees
      delay(80000);
      servo4.write(0); // Set servo4 to 0 degrees
      
      // Print a reminder of the currently running servo
      Serial.println("Servo 4 is running. Fruiting Stage");
    }
}



void setup() {
  Serial.begin(115200);

  // Attach the servos to the respective pins
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  servo3.attach(servo3Pin);
  servo4.attach(servo4Pin);

  connectToWiFi();
}

void loop() {

if ((currentHour == 8 && currentMinute == 0) || (currentHour == 8 && currentMinute == 40) || (currentHour == 9 && currentMinute == 20)) {
    // Run the two functions
    getCurrentGrowthStage();
    controlServos();
  }

  delay(60000); // Delay for 1 minute before checking again
}

