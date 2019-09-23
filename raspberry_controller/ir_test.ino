#define SENSORPIN 4

int sensorState = 0, lastState=0;         // variable for reading the pushbutton status
void setup() {
    pinMode(SENSORPIN, INPUT);
    digitalWrite(SENSORPIN, HIGH); // turn on the pullup
    Serial.begin(9600);
}

void loop(){
  // read the state of the pushbutton value:
  sensorState = digitalRead(SENSORPIN);

  if (sensorState && !lastState) {
    Serial.println("Unbroken");
  }
  if (!sensorState && lastState) {
    Serial.println("Broken");
  }
  lastState = sensorState;
}