/*
 * Taylor Harper
 * University of Texas at San Antonio
 *
 * This code performs different mechanical functions as needed by the sorter project.
 * The code will drive the following:
 *  1. A string of LED lights
 *  2. Three different continuous rotary encoders
 *  3. An absolute rotary encoder
 *
 *  All  code (after initialization) will be changed via serial command from the onboard Raspberry Pi
 *  The letter based codes for the switch are as following:
 *      -a --- Stop Camera Servo
 *      -b --- Stop Feeder Servo
 *      -c --- Stop Hopper Servo
 *      -d --- Stop Sorter Servo
 *      -e --- Run Camera Servo
 *      -f --- Run Camera Servo (Reverse)
 *      -g --- Run Feeder Servo
 *      -h --- Run Hopper Servo
 *      -i --- Run Sorter Servo
 *      -j --- Turn off LED lights
 *      -k --- Change LED Lights to white
 *      -l --- Change LED Lights to red
 *      -m --- Change LED Lights to color pattern change
 *
 *  TODO: If try-catch alternative is needed then check out --> http://www.on-time.com/ddj0011.htm
 *  TODO: May need a failsafe if the serial connection is broken
 */

#include <Servo.h>

// Initialize the four different servos
Servo camera_servo feeder_servo hopper_servo sorter_servo;

int camera_servo_pos = 0;
int feeder_servo_pos = 0;
int hopper_servo_pos = 0;
int sorter_servo_pos = 0;

void setup() {
    Serial.begin(9600);

    // Initialize the servos and attach them to their corresponding pins
    camera_servo.attach(5);
    feeder_servo.attach(6);
    hopper_servo.attach(7);
    sorter_servo.attach(8);
}

void loop() {
    // When a command is received from the serial port, perform the corresponding action and respond.
    if (Serial.available() > 0) {
        // Read the received byte
        rec_byte = Serial.read();

        // Determine action based on received byte
        switch (range) {
            case "a": // Stop Camera Servo
                camera_servo.write(88);
                Serial.print("Camera Encoder - Stopped");
                break;
            case "b": // Stop Feeder Servo
                feeder_servo.write();
                Serial.print("Feeder Encoder - Stopped");
                break;
            case "c": // Stop Hopper Servo
                hopper_servo.write();
                Serial.print("Hopper Encoder - Stopped");
                break;
            case "d": // Stop Sorter Servo
                sorter_servo.write();
                Serial.print("Sorter Encoder - Stopped");
                break;
            case "e": // Run Camera Servo
                camera_servo.write();
                Serial.print("Camera Encoder - Running");
                break;
            case "f": // Run Camera Servo (Reverse)
                camera_servo.write();
                Serial.print("Camera Encoder - Running (Reverse)")
            case "g": // Run Feeder Servo
                feeder_servo.write();
                Serial.print("Feeder Encoder - Running");
                break;
            case "h": // Run Hopper Servo
                hopper_servo.write();
                Serial.print("Hopper Encoder - Running");
                break;
            case "i": // Run Sorter Servo
                sorter_servo.write();
                Serial.print("Sorter Encoder - Running");
                break;
            case "j": // Turn off LED lights
                // TODO: Write this
                Serial.print("LED - Off");
                break;
            case "k": // Change LED Lights to white
                // TODO: Write this
                Serial.print("LED - White");
                break;
            case "l": // Change LED Lights to red
                // TODO: Write this
                Serial.print("LED - Red");
                break;
            case "m": // Change LED Lights to color pattern change
                // TODO: Write this
                Serial.print("LED - Pattern")
                break;
        }
}