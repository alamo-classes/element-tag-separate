#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
 #include <avr/power.h>
#endif

/*****************************************************************
 *                  Pin Assignments                   *
*****************************************************************/
#define SENSORPIN 4
byte SERVO_PIN = A5;
byte SERVO_FEEDBACK_PIN = 6;
byte LED_PIN = 9;
byte CAMERA_SERVO = 47;
byte FEEDER_SERVO = 37;
byte HOPPER_SERVO = 35;
/*****************************************************************
 *                  Continuous Servo Variables                   *
*****************************************************************/
Servo camera_servo;
Servo feeder_servo;
Servo hopper_servo;

/*****************************************************************
 *                  Absolute Servo Variables                   *
*****************************************************************/
Servo sorter_servo;
int rec_byte = 0;
float DUTY_SCALE = 1000;
unsigned long DUTY_CYCLE_MIN = 29;  // 2.9% * DUTY_SCALE
unsigned long DUTY_CYCLE_MAX = 971; // 9.71% * DUTY_SCALE
float UNITS_IN_FULL_CIRCLE = 360;   // Because 360 degrees are in a circle
int ERROR_ANGLE_OFFSET_US = 23;
float CONSTANT_KP = .7;
int MIN_PULSE_SPEED_OFFSET_US = -40;    // Going Counter-clockwise a bit - can be smaller ( < -40)
int MAX_PULSE_SPEED_OFFSET_US = 40;     // Going Clockwise  a bit - can be bigger (> 40)
int HOLD_STILL_PULSE_SPEED_US = 1500;   // HOLD_STILL is for keeping the servo in place (no movement, don't change)
int ANGLE_Q2_MIN = 90;
int ANGLE_Q3_MAX = 270;
int sorter_servo_angle = 355;
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

/*****************************************************************
 *                  IR Detector Variables                   *
*****************************************************************/
int sensorState = 1;

/*****************************************************************
 *                  LED Variables                   *
*****************************************************************/
Adafruit_NeoPixel strip(16, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
    // Start LEDs
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

    // Start continuous servos and set rotation to neutral
    camera_servo.attach(CAMERA_SERVO);
    feeder_servo.attach(FEEDER_SERVO);
    hopper_servo.attach(HOPPER_SERVO);

    camera_servo.write(91);
    feeder_servo.write(90);
    hopper_servo.write(90);

    // Start absolute servo
    pinMode(SERVO_FEEDBACK_PIN, INPUT);
    sorter_servo.attach(SERVO_PIN);

    // Start IR Detector
    pinMode(SENSORPIN, INPUT);
    digitalWrite(SENSORPIN, HIGH);

    // Start serial connection
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0 ) {
        // Read byte from received serial message
        rec_byte = Serial.read();

        // Determine action based on received byte
        switch (rec_byte) {
            case 'a': // Run Detection Loop
                // Reset the sensorState
                sensorState = 1;
                // Start the motors
                camera_servo.write(100);
                hopper_servo.write(91);
                feeder_servo.write(100);
                // Wait on the block to be detected
                while (sensorState && (Serial.available() == 0)) {
                    sensorState = digitalRead(SENSORPIN);
                }
                // If an interrupt was sent by the raspberry pi controller, stop motors and break from routine
                if (sensorState) {
                    camera_servo.write(90);
                    hopper_servo.write(90);
                    feeder_servo.write(90);
                    break;
                } else {
                // Slow the servos
                camera_servo.write(96);
                hopper_servo.write(90);
                feeder_servo.write(90);
                // Wait till part gets into position, then stop the servo
                delay(3000);
                camera_servo.write(91);
                Serial.println("Detected, Detected, Detected");
                break;
                }
            case 'b': // Move part off of belt
                move_camera_belt();
                break;
            case 'c': // Stop all servos
                camera_servo.write(90);
                hopper_servo.write(90);
                feeder_servo.write(90);
                break;
            case '1': // Move block to bin #1
                sorter_servo_angle = 350;
                // While errorAngle is out of range move the servo
                break;
            case '2': // Move block to bin #1
                sorter_servo_angle = 315;
                // While errorAngle is out of range move the servo
                break;
            case '3': // Move block to bin #1
                sorter_servo_angle = 285;
                // While errorAngle is out of range move the servo
                break;
            case '4': // Move block to bin #1
                sorter_servo_angle = 255;
                // While errorAngle is out of range move the servo
                break;
            case '5': // Move block to bin #1
                sorter_servo_angle = 220;
                // While errorAngle is out of range move the servo
                break;
            case '6': // Move block to bin #1
                sorter_servo_angle = 180;
                // While errorAngle is out of range move the servo
                break;
            case '7': // Move block to bin #1
                sorter_servo_angle = 40;
                // While errorAngle is out of range move the servo
                break;
            default:
                Serial.println("Unknown command");
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

  outputSpeed = HOLD_STILL_PULSE_SPEED_US + outputSpeed + offset;
  sorter_servo.writeMicroseconds(outputSpeed);

  delay(20);  // control signal pulses should be about every 20 ms
}

void move_camera_belt(){
    camera_servo.write(105);
    delay(2000);
    camera_servo.write(90);
}