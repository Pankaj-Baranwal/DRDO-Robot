#include <Servo.h> 

volatile int left_encoder = 0;
volatile int right_encoder = 0;
// Include the Servo library 
// Declare the Servo pin 

int servoPin = 7; 
// Create a servo object 
Servo Servo1;

int encoder_left = 23, encoder_right = 22;
int pin_left1 = 29, pin_left2 = 33, pwm_left3 = 31;
int pin_right1 = 35, pin_right2 = 39, pwm_right3 = 37;
int counter = 0;

void setup(){
  Serial.begin(9600);
 // We need to attach the servo to the used pin number 
  Servo1.attach(servoPin); 
  pinMode(pin_left1, OUTPUT);
  pinMode(pin_left2, OUTPUT);
  pinMode(pwm_left3, OUTPUT);
  pinMode(pin_right1, OUTPUT);
  pinMode(pin_right2, OUTPUT);
  pinMode(pwm_right3, OUTPUT);
  analogWrite(pwm_left3, 130);
  analogWrite(pwm_right3, 130);
  pinMode(encoder_left, INPUT);
  pinMode(encoder_right, INPUT);
}

void loop(){
  if(Serial.available() > 0){
    String data = Serial.readString();  
    Serial.print(data);
    if(data == "a"){
      move_to_cell(1);
      Serial.write("t");
    }else if(data == "b"){
      move_to_cell(2);
      Serial.write("t");
    }else if(data == "c"){
      move_to_cell(3);
      Serial.write("t");
    }else if(data == "d"){
      move_to_cell(4);
      Serial.write("t");
    }else if(data == "e"){
      move_to_cell(5);
      Serial.write("t");
    }else if(data == "f"){
      move_to_cell(6);
      Serial.write("t");
    }else if(data == "g"){
      move_to_cell(7);
      Serial.write("t");
    }else if(data == "h"){
      move_to_cell(8);
      Serial.write("t");
    }else if(data == "i"){
      move_to_cell(9);
      Serial.write("t");
    }else if(data == "l"){
      move_pycam(180);
      Serial.write("t");
    }else if(data == "r"){
      move_pycam(0);
      Serial.write("t");
    }else if(data == "z"){
      move_pycam(90);
      Serial.write("t");
    }else{
      Serial.write("f");
    }       
  }
}

void move_to_cell(int x){
  int forty_five = 20;
  int distance = 30;
  if (x == 1){
    left(forty_five);
    delay(1000);
    forward(distance);
  }else if (x == 2){
    forward(distance);
  }else if (x == 3){
    right(forty_five);
    delay(1000);
    forward(distance);
  }else if (x == 4){
    left(forty_five*2);
    forward(distance);
  }else if(x == 5){
    stop_all();
  }else if (x == 6){
    right(forty_five*2);
    forward(distance);
  }else if(x == 7){
    left(forty_five*3);
    delay(1000);
    forward(distance);
  }else if(x == 8){
    left(forty_five*4);
    forward(distance);
  }else if(x == 9){
    right(forty_five*3);
    forward(distance);
  }
}

void forward(int encoder_count){
  left_encoder = 0;
  volatile int prev = 0;
  volatile int curr = 0;
  
  while(left_encoder < encoder_count) {
    curr = digitalRead(encoder_left);
    if (prev != curr){
       prev = curr;
       left_encoder++;
    }
    
    digitalWrite(pin_left1, LOW);
    digitalWrite(pin_left2, HIGH);
    digitalWrite(pin_right1, LOW);
    digitalWrite(pin_right2, HIGH);
  }
  stop_all();
}

void left(int encoder_count){
  left_encoder = 0;
  volatile int prev = 0;
  volatile int curr = 0;
  
  while(left_encoder < encoder_count) {
    curr = digitalRead(encoder_left);
    if (prev != curr){
       prev = curr;
       left_encoder++;
    }
    digitalWrite(pin_left1, LOW);
    digitalWrite(pin_left2, HIGH);
    digitalWrite(pin_right1, HIGH);
    digitalWrite(pin_right2, LOW);
  }
  stop_all();
}

void right(int encoder_count){
  left_encoder = 0;
  volatile int prev = 0;
  volatile int curr = 0;
  
  while(left_encoder < encoder_count) {
    curr = digitalRead(encoder_left);
    if (prev != curr){
       prev = curr;
       left_encoder++;
    }
    digitalWrite(pin_left1, HIGH);
    digitalWrite(pin_left2, LOW);
    digitalWrite(pin_right1, LOW);
    digitalWrite(pin_right2, HIGH);
  }
  stop_all();
}

void move_pycam(int degrees){
    // Make servo go to 0 degrees 
  Servo1.write(degrees);
  delay(2000);
}

void stop_all(){
  digitalWrite(pin_left1, LOW);
  digitalWrite(pin_left2, LOW);
  digitalWrite(pin_right1, LOW);
  digitalWrite(pin_right2, LOW);  
}
