const int TRIG_PIN = 5;
const int ECHO_PIN = 18;
const int IN1 = 12;
const int IN2 = 14;

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  Serial.println(distance);

  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'S') { 
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
    } 
    else if (cmd == 'F') { 
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
    }
  }
  delay(50); 
}