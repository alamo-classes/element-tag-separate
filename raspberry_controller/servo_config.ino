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
 *      -d --- Set Sorter Servo
 *      -e --- Run Camera Servo
 *      -f --- Run Camera Servo (Reverse)
 *      -g --- Run Feeder Servo
 *      -h --- Run Hopper Servo
 *      -i --- Turn off LED lights
 *      -j --- Change LED Lights to white
 *      -k --- Change LED Lights to red
 *      -l --- Change LED Lights to color pattern change
 *      -m --- Begin IR sensor loop
 *
 *  TODO: If try-catch alternative is needed then check out --> http://www.on-time.com/ddj0011.htm
 *  TODO: May need a failsafe if the serial connection is broken
 */

#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
 #include <avr/power.h>
#endif

// Initialize the LED
Adafruit_NeoPixel strip(16, 9, NEO_GRB + NEO_KHZ800);
byte SERVO_PIN = A5;
byte SERVO_FEEDBACK_PIN = 6;

// Initialize the four different servos
Servo camera_servo;
Servo feeder_servo;
Servo hopper_servo;
Servo sorter_servo;

// Second byte for sorter serial read
int rec_byte = 0;
float DUTY_SCALE = 1000;
unsigned long DUTY_CYCLE_MIN = 29;  // 2.9% * DUTY_SCALE
unsigned long DUTY_CYCLE_MAX = 971; // 9.71% * DUTY_SCALE
float UNITS_IN_FULL_CIRCLE = 360;   // Because 360 degrees are in a circle

// Tune the vars below for controlling how fast the servo gets to the right place and stays there
int ERROR_ANGLE_OFFSET_US = 23;
float CONSTANT_KP = 0.9;
int MIN_PULSE_SPEED_OFFSET_US = -40;    // Going Counter-clockwise a bit - can be smaller ( < -40)
int MAX_PULSE_SPEED_OFFSET_US = 40;     // Going Clockwise  a bit - can be bigger (> 40)
int HOLD_STILL_PULSE_SPEED_US = 1500;   // HOLD_STILL is for keeping the servo in place (no movement, don't change)

// Angles for different quadrants around the unit circle (for counting number of turns)
int ANGLE_Q2_MIN = 90;
int ANGLE_Q3_MAX = 270;
char sorter_servo_pos = "1";
int sorter_servo_angle = 180;
int currentAngle = 0;                   // The angle the servo is at
int prevAngle = 0;                      // The last angle the servo had
int errorAngle = 0;                     // How off we are from the target angle
int turns = 0;                          // How many times we've gone around the circle

unsigned long tHigh;
unsigned long tLow;
unsigned long tCycle;
float dutyCycle;
float maxUnitsForCircle;
int outputSpeed;

// IR Detector Sensor
int sensorState = 0;

void setup() {
    // Start serial connection
    Serial.begin(9600);

    // Initialize the LED lights
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
#endif
    strip.begin();
    strip.show();
    strip.setBrightness(75);
    for (int i=0; i<strip.numPixels(); i++) {
        // Set all pixels to white
        strip.setPixelColor(i, strip.Color(127, 127, 127));
    }
    strip.show();


    // Initialize the servos and attach them to their corresponding pins
    camera_servo.attach(47);
    camera_servo.write(90);
    feeder_servo.attach(37);
    feeder_servo.write(90);
    hopper_servo.attach(35);
    hopper_servo.write(90);

    sorter_servo.attach(SERVO_PIN);
    pinMode(SERVO_FEEDBACK_PIN, INPUT);

    pinMode(4, HIGH)
}

void loop() {
    // When a command is received from the serial port, perform the corresponding action and respond.
    if (Serial.available() > 0) {
        // Read the received byte
        rec_byte = Serial.read();

        // Determine action based on received byte
        switch (rec_byte) {
            case 'a': // Stop Camera Servo
                camera_servo.write(90);
                Serial.print("Camera Encoder - Stopped");
                break;
            case 'b': // Stop Feeder Servo
                feeder_servo.write(90);
                Serial.print("Feeder Encoder - Stopped");
                break;
            case 'c': // Stop Hopper Servo
                hopper_servo.write(90);
                Serial.print("Hopper Encoder - Stopped");
                break;
            case 'd': // Set Sorter Servo
                sorter_servo_pos = Serial.read();
                switch (sorter_servo_pos)
                    case '1':
                        sorter_servo_angle = 0;
                        Serial.print("Sorter Encoder - Set Position #1");
                        break;
                    case '2':
                        sorter_servo_angle = 90;
                        Serial.print("Sorter Encoder - Set Position #2");
                        break;
                    case '3':
                        sorter_servo_angle = 120;
                        Serial.print("Sorter Encoder - Set Position #3");
                        break;
                break;
            case 'e': // Run Camera Servo
                camera_servo.write(100);
                Serial.print("Camera Encoder - Running");
                break;
            case 'f': // Run Camera Servo (Reverse)
                camera_servo.write(100);
                Serial.print("Camera Encoder - Running (Reverse)");
            case 'g': // Run Feeder Servo
                feeder_servo.write(100);
                Serial.print("Feeder Encoder - Running");
                break;
            case 'h': // Run Hopper Servo
                hopper_servo.write(100);
                Serial.print("Hopper Encoder - Running");
                break;
            case 'i': // Turn off LED lights
                strip.clear();
                strip.show();
                Serial.print("LED - Off");
                break;
            case 'j': // Change LED Lights to white
                for (int i=0; i<strip.numPixels(); i++) {
                    strip.setPixelColor(i, strip.Color(127, 127, 127));
                }
                strip.show();
                Serial.print("LED - White");
                break;
            case 'k': // Change LED Lights to red
                for (int i=0; i<strip.numPixels(); i++) {
                    // Set all pixels to white
                    strip.setPixelColor(i, strip.Color(127, 0, 0));
                    }
                strip.show();
                Serial.print("LED - Red");
                break;
            case 'l': // Change LED Lights to color pattern change
                // TODO: Write this
                Serial.print("LED - Pattern");
                break;
            case 'm':
                while (Serial.available()  < 1){
                    sensorState = digitalRead(4);
                    if (sensorState) {
                        Serial.print("sensorState is high")
//                         delay(500)
//                         Check it again
                    } else {
                        Serial.print("sensorState is low")
                    }
                }
            default: // Replay that the byte was invalid
                Serial.print("Invalid byte detected...");
                break;
        }
    }
    feedback_servo(sorter_servo_angle);
}

void feedback_servo(int targetAngle) {
 // Run pulseWidth measuring to figure out the current angle of the servo
  tHigh = pulseIn(SERVO_FEEDBACK_PIN, HIGH);
  tLow = pulseIn(SERVO_FEEDBACK_PIN, LOW);
  tCycle = tHigh + tLow;
  // Check if our cycle time was appropriate
  if (!(tCycle > 1000 && tCycle < 1200)) {
    // Invalid cycle time, so try pulse measuring again
    // Serial.println("Invalid cycle time");
    return;
  }
  // Calculate the duty cycle of the pulse
  dutyCycle = (DUTY_SCALE) * ((float) tHigh / tCycle);
  maxUnitsForCircle = UNITS_IN_FULL_CIRCLE - 1;

  // Calculate exact angle of servo
  currentAngle = maxUnitsForCircle - ((dutyCycle - DUTY_CYCLE_MIN) * UNITS_IN_FULL_CIRCLE) / ((DUTY_CYCLE_MAX - DUTY_CYCLE_MIN) + 1);

  // Clip current angle if we're somehow above or below range
  if (currentAngle < 0) {
    currentAngle = 0;
  } else if (currentAngle > maxUnitsForCircle) {
    currentAngle = maxUnitsForCircle;
  }

  // Handle quadrant wrap q1 -> q4 and q4 -> q1, to count turns
  if ((currentAngle < ANGLE_Q2_MIN) && (prevAngle > ANGLE_Q3_MAX)) {
    turns += 1;
  } else if ((prevAngle < ANGLE_Q2_MIN) && (currentAngle > ANGLE_Q3_MAX)) {
    turns -= 1;
  }

  // Save previous position
  prevAngle = currentAngle;
  errorAngle = targetAngle - currentAngle;

  // Simple P Controller
  outputSpeed = errorAngle * CONSTANT_KP;

  if (outputSpeed > MAX_PULSE_SPEED_OFFSET_US) {
    outputSpeed = MAX_PULSE_SPEED_OFFSET_US;
  } else if (outputSpeed < MIN_PULSE_SPEED_OFFSET_US) {
    outputSpeed = MIN_PULSE_SPEED_OFFSET_US;
  }

  int offset = 0;
  if (errorAngle > 0) {
    offset = ERROR_ANGLE_OFFSET_US;
  } else if (errorAngle < 0) {
    offset = -1 * ERROR_ANGLE_OFFSET_US;
  }

//   Serial.print("Current angle: ");
//   Serial.print(currentAngle);
//   Serial.print(" / ");
//   Serial.print(errorAngle);

  outputSpeed = HOLD_STILL_PULSE_SPEED_US + outputSpeed + offset;
  sorter_servo.writeMicroseconds(outputSpeed);

  delay(20);  // control signal pulses should be about every 20 ms
}