
int echo = 6;
int trigger = 7;
int motor_righta = 2;
int motor_rightb = 3;
int motor_lefta = 5;
int motor_leftb = 4;
int motor_speed = 120;
int motor_speed_right = 140;


// the setup routine runs once when you press reset:
void setup() {
  Serial.begin(115200);
  pinMode(motor_righta, OUTPUT);
  pinMode(motor_rightb, OUTPUT);
  pinMode(motor_lefta, OUTPUT);
  pinMode(motor_leftb, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  Serial.println("In loop");
  long value_ultrasonic = ultrasonic();
  if(value_ultrasonic < 50 && value_ultrasonic > 10){
    forward();
    delay(100);
  }
  else if(ultrasonic() > 50){
    left(800);
    if(ultrasonic() > 50){
      right(1300);
    }
  }else{
    stop_motors();
  }
}

void forward() {
  digitalWrite(motor_lefta, LOW);
  analogWrite(motor_leftb, motor_speed);
  digitalWrite(motor_righta, LOW);
  analogWrite(motor_rightb, motor_speed_right);
}

void reverse(){
  digitalWrite(motor_lefta, motor_speed);
  digitalWrite(motor_leftb, LOW);
  digitalWrite(motor_righta, motor_speed_right);
  digitalWrite(motor_rightb, LOW);
}

void left(int time){
  Serial.println("Left");
  digitalWrite(motor_lefta, LOW);
  digitalWrite(motor_leftb, LOW);
  digitalWrite(motor_righta, LOW);
  analogWrite(motor_rightb, motor_speed_right);
  delay(time);
}
void right(int time){
  Serial.println("Right");
  digitalWrite(motor_lefta, LOW);
  analogWrite(motor_leftb, motor_speed);
  digitalWrite(motor_righta, LOW);
  digitalWrite(motor_rightb, LOW);
  delay(time);
}

double ultrasonic(){ 
  long duration, cm;
  
  pinMode(trigger, OUTPUT);
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  
  pinMode(echo, INPUT);
  duration = pulseIn(echo, HIGH);

  cm = duration / 29 / 2;
  Serial.println(cm);
  return cm;
}

void stop_motors(){
  digitalWrite(motor_lefta, LOW);
  digitalWrite(motor_leftb, LOW);
  digitalWrite(motor_righta, LOW);
  digitalWrite(motor_rightb, LOW);
}
