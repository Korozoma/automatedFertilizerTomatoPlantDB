#include <Servo.h>

Servo servoMotor;  // Create a servo object

const int servoPin = D3;  // Pin D3 on NodeMCU

void setup() {
  servoMotor.attach(servoPin);  // Attaching the servo to the specified pin
}

void loop() {
  moveServo(30);   // Move servo to 90 degrees
  delay(5000);     // Wait for 5 seconds
  moveServo(0);    // Move servo back to 0 degrees
  delay(5000);     // Wait for 5 seconds
}

void moveServo(int degrees) {
  int pos = map(degrees, 0, 180, 0, 180);  // Map the angle to servo position
  servoMotor.write(pos);                   // Move the servo to the desired position
}