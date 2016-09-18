#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

#include <Encoder.h>

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 mpu;

#define OUTPUT_READABLE_EULER


//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(3, 7);

long positionLeft  = -999;


//Defined for IMU

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer


Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
float init_imu;

long knobVal = 0;
// for motor movement
int rf =9 ,rb =10,lf=5,lb=6;
int motor_speed =150; //(0-255)

// for PID
int power_difference, encoderleft, encoderright, proportional;
int base, next;
const int maximum = 150;


// for encoders
double unit_distance = 31.415/10000;

int deg_dis = 3;
int x;
int y;
int a, b;

long enc_rtcount = 0, enc_ltcount = 0;
int r_en = 7, l_en = 3;


int count = 0;
float deg1 =0;

void dmpDataReady() {
    mpuInterrupt = true;
}

void setup() {
  // BEGIN IMU INIT
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
      TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz)
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif
  Serial.begin(115200);

  while (!Serial); // wait for Leonardo enumeration, others continue immediately
  Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();

  Serial.println(F("Testing device connections..."));
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));


  Serial.println(F("\nSend any character to begin DMP programming and demo: "));
  while (Serial.available() && Serial.read()); // empty buffer
//  while (!Serial.available());                 // wait for data
//  while (Serial.available() && Serial.read()); // empty buffer again

  Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788); // 1688 factory default for my test chip

  if (devStatus == 0) {
      Serial.println(F("Enabling DMP..."));
      mpu.setDMPEnabled(true);

      Serial.println(F("Enabling interrupt detection (Arduino external interrupt 0)..."));
      attachInterrupt(0, dmpDataReady, RISING);
      mpuIntStatus = mpu.getIntStatus();

      Serial.println(F("DMP ready! Waiting for first interrupt..."));
      dmpReady = true;

      packetSize = mpu.dmpGetFIFOPacketSize();
  }
  else {
      Serial.print(F("DMP Initialization failed (code "));
      Serial.print(devStatus);
      Serial.println(F(")"));
  }
  // END IMU INIT
  
  // encoder pins
  pinMode(r_en, INPUT);
  pinMode(l_en, INPUT);
  // motor pins
  pinMode(lf, OUTPUT);
  pinMode(lb, OUTPUT);
  pinMode(rf, OUTPUT);
  pinMode(rb, OUTPUT);
  
  while(millis() < 20000) {
    init_imu = imu_read();
  }
  base = imu_read();
}


void loop() {
  if (count == 0) {
    imu_read();
//    forward_movt(110);
    forward_movt_using_imu(360);

//    forward_movt(50);
//    forward_movt_using_imu(90);
//    forward_movt(50);
//    forward_movt_using_imu(90);
//    forward_movt(50);
    count =1;
  }
}

void forward_movt_using_imu (int dist){
  double initial = imu_read();
  double previous = initial;
  double current = previous;
  double total = 0;
  if (dist > 0){
    while(total < dist-0.8) {
      current = imu_read();
      Serial.println("CURRENT");
      Serial.println(current);
      Serial.println("PREVIOUS");
      Serial.println(previous);
      if (current != 0){
      if (current <15 && previous > 345){
        if (abs(current + 360 - previous) < 15){
          total = total + abs(current + 360 - previous);
        }
      }
      else if (current > 345 && previous < 15){
        if (abs(previous + 360 - current) < 15){
          total = total + abs(previous + 360 - current);
        }
      }
      else{
        if (abs(current - previous) < 15){
          total = total + abs(current - previous);
        }
      }
      Serial.println("TOTAL");
      Serial.println(total);
      previous = current;
      }
      turn_left();
    }
  }else{
    dist = abs(dist);
    while(total < dist-0.8) {
      current = imu_read();
      Serial.println("CURRENT");
      Serial.println(current);
      Serial.println("PREVIOUS");
      Serial.println(previous);
      if (current != 0){
      if (current <15 && previous > 345){
        if (abs(current + 360 - previous) < 15){
          total = total + abs(current + 360 - previous);
        }
      }
      else if (current > 345 && previous < 15){
        if (abs(previous + 360 - current) < 15){
          total = total + abs(previous + 360 - current);
        }
      }
      else{
        if (abs(current - previous) < 15){
          total = total + abs(current - previous);
        }
      }
      Serial.println("TOTAL");
      Serial.println(total);
      previous = current;
      }
      turn_right();
    }
  }
  
  if (final < dist && abs(initial-360) <dist){
    if (final + abs(360 - initial) - dist > 2){
      
    }else if (abs(final + abs (360 - initial) - dist) > 2){
      
    }
  }else if(initial < dist && abs(final - 360) < dist){
    if (initial + abs(360 - final) - dist > 2){
      
    }else if (abs(initial + abs (360 - final) - dist) > 2){
      
    }    
  }else{
    
  }
  
  enc_ltcount = 0;
  sstop();
  deg1=0;
  imu_read();
  knobLeft.write(0);
  base = imu_read();
}

void forward_movt (int dist){
  long no_of_spokes = (long)(dist/unit_distance);
//  1 degree, spokes covered = .67; total spokes covered in x deg = .67*x
  knobLeft.write(0);
  Serial.println("INITIAL KNOB COUNT");
  Serial.println(no_of_spokes);
  enc_ltcount = knobLeft.read();
  knobVal = enc_ltcount;
  no_of_spokes = enc_ltcount + no_of_spokes;
  Serial.println("INITIAL NUMBER OIF SPOKES");
  Serial.println(no_of_spokes);
  while(abs(enc_ltcount) <= abs(no_of_spokes)) {
    call_ltenc();
    next = imu_read_off();
       if(next<180)
       {proportional = next ;
       }else if(next>=180)
       {
         proportional=next-360;
       }
    power_difference = proportional*25;

    if (power_difference > maximum)
      power_difference = maximum;
    if (power_difference < -maximum)
      power_difference = -maximum;    
    forward();
  }
  enc_ltcount = 0;
  sstop();
  deg1=0;
  knobLeft.write(0);
}

void turn_left(){
  analogWrite(rf, motor_speed);
  analogWrite(rb, LOW);
  analogWrite(lf, LOW);
  analogWrite(lb, LOW);
}

void turn_right(){
  analogWrite(rf, LOW);
  analogWrite(rb, LOW);
  analogWrite(lf, motor_speed);
  analogWrite(lb, LOW);
}

void forward(){
  if (power_difference < 0)//moving left -----errooor 
  {
    analogWrite(rf, (maximum + power_difference));  ////////////right motor at less speed so that bot moves right
    analogWrite(rb,LOW);
    analogWrite(lf, maximum);
    analogWrite(lb,LOW);
    Serial.print("\t\t\t\t\tleft");
  }
  else //moving right -------errror
  {
    analogWrite(rf,maximum);
    analogWrite(rb, LOW);
    analogWrite(lf, maximum - power_difference);/// left motor is at less speed so that bot moves left
    analogWrite(lb, LOW);
    Serial.print("\t\t\t\t\tright");
  }
} 

void turn_right(float deg) {
  base += deg;
  forward_movt_using_imu(deg);
}

void turn_left(float deg) {
  base -= deg;
  deg1+=deg;
}

int call_rtenc() {
  b = a;
  a = digitalRead(r_en);
  
  if((a == 0 && b == 1) || (a == 1 && b == 0)) {
    enc_rtcount++;
  }
  return enc_rtcount;
}

void call_ltenc() {
  long prev = knobVal;
  knobVal = knobLeft.read();
  Serial.println("Prev Values: ");
  Serial.println(prev);
  Serial.println(knobVal);
  enc_ltcount = enc_ltcount + abs(abs(knobVal) - abs(prev));
  Serial.println("ENCODER COUNT");
  Serial.println(enc_ltcount);
}

void sstop() {
  digitalWrite(lf,LOW);
  digitalWrite(lb,LOW);
  digitalWrite(rb,LOW);
  digitalWrite(rf,LOW);
}

float imu_read(){
 if (!dmpReady) return 0;
    while (!mpuInterrupt && fifoCount < packetSize) {
    }


    mpuInterrupt = false;
    mpuIntStatus = mpu.getIntStatus();


    fifoCount = mpu.getFIFOCount();

    if ((mpuIntStatus & 0x10) || fifoCount == 1024) {

        mpu.resetFIFO();
        Serial.println(F("FIFO overflow!"));


    } else if (mpuIntStatus & 0x02) {

        while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();


        mpu.getFIFOBytes(fifoBuffer, packetSize);
        fifoCount -= packetSize;

        #ifdef OUTPUT_READABLE_EULER
            // display Euler angles in degrees
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetEuler(euler, &q);
            if (euler[0]*180/M_PI <0){
              float neg_deg = euler[0]*180/M_PI +360;
              Serial.print("euler\t");
              Serial.println(neg_deg);
              return neg_deg;
            }
            else{
              Serial.print("euler\t");
              Serial.println(euler[0] * 180/M_PI);
              return  euler[0]*180/M_PI;
            }
         #endif
    }
}

float imu_read_off() {
  float check = imu_read();
  check = check - base;
  
  if (check < 0) {
    check += 360;
  }
 // Serial.println(check);
  return check;
}

