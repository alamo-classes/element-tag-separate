#define SENSORPIN 4

int sensorState = 0, lastState=0;         // variable for reading the pushbutton status
void setup() {
    pinMode(SENSORPIN, INPUT);
    digitalWrite(SENSORPIN, HIGH); // turn on the pullup
    Serial.begin(9600);
}

void loop(){
  // read the state of the pushbutton value. output 0 is detection
  sensorState = digitalRead(SENSORPIN);
  if (!sensorState) {
    Serial.print("!");
    delay(1000);
  }