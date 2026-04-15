#include <Servo.h>
#include <Wire.h>

#define Apin 9
#define Bpin 10
#define Cpin 11
#define EEpin 5

#define control1 A0
#define control2 A1

#define lengthA 100
#define lengthB 100
#define lengthC 10

Servo servoA, servoB, servoC, servoEE;

float theta1, theta2, theta3;
float thetadamp1, thetadamp2, thetadamp3;
float thetaprev1, thetaprev2, thetaprev3;
int prevX, prevY, open; 
int Xcoord = 100, Ycoord = 100;

int setpoint1 = 90, setpoint2 = 180;
float damping = 0.05;

bool reached;

byte address = 0x10;

void setup(){
  servoA.attach(Apin);
  servoB.attach(Bpin);
  servoC.attach(Cpin);
  servoEE.attach(EEpin);
  pinMode(control1, INPUT_PULLUP);
  pinMode(control2, INPUT_PULLUP);

  servoA.write(setpoint1);
  servoB.write(setpoint2);
  servoC.write(setpoint1);
  servoEE.write(0);

  thetaprev1 = setpoint1;
  thetaprev2 = setpoint1;
  thetaprev3 = setpoint1;

  Wire.begin(10);
  Wire.onReceive(reachTarget);

  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    Xcoord = Serial.parseInt();
    Ycoord = Serial.parseInt();
    open = Serial.parseInt();

    if (Serial.peek() == '\n' || Serial.peek() == '\r'){
      Serial.read();
    }

    Serial.println("Received");
  }

  int Ynewcoord = Ycoord + 10;
  float cos2 = (pow(Xcoord, 2) + pow(Ynewcoord, 2) - pow(lengthA, 2) - pow(lengthB, 2))/(2*lengthA*lengthB);
  theta2 = -acos(cos2);
  theta1 = atan2(Ynewcoord, Xcoord) - atan2(lengthB*sin(theta2), lengthB*cos2 + lengthA);
  theta3 = -PI/2 - theta2 - theta1;

  theta1 = theta1*180/PI;
  theta2 = theta2*180/PI;
  theta3 = theta3*180/PI;

  float shiftA = setpoint1 - theta1;
  float shiftB = setpoint2 + theta2;
  float shiftC = setpoint1 + theta3;

  theta1 = setpoint1 - shiftA;
  theta2 = shiftB;
  theta3 = setpoint1 - shiftC;

  thetadamp1 = theta1 - thetaprev1;
  thetaprev1 = thetaprev1 + (thetadamp1 * damping);
  
  thetadamp2 = theta2 - thetaprev2;
  thetaprev2 = thetaprev2 + (thetadamp2 * damping);
  
  thetadamp3 = theta3 - thetaprev3;
  thetaprev3 = thetaprev3 + (thetadamp3 * damping);

  if( thetaprev1 > 20 && thetaprev2 > 20){
    servoA.write(thetaprev1);
    servoB.write(thetaprev2);
    servoC.write(thetaprev3);
  }

  if (abs(thetadamp1) + abs(thetadamp2) + abs(thetadamp3) < 5 && !reached){
    Serial.print(" Reached: ");
    Serial.print("X =  ");
    Serial.print(Xcoord);
    Serial.print(" ,");
    Serial.print("Y =  ");
    Serial.println(Ynewcoord);

    prevX = Xcoord;
    prevY = Ycoord;

    reached = true;

    if (open){
      delay(1000);
      servoEE.write(50);
      delay(1000);
      servoEE.write(40);
      delay(1000);
      servoEE.write(30);
      delay(1000);
      servoEE.write(20);
      delay(1000);
      servoEE.write(0);
      delay(1000);
      reachDefault();
    }
  }
  else {
    if (prevX != Xcoord && prevY != Ycoord){
      reached = false;

      if (open == 1)
        servoEE.write(60);
    }
  }

  delay(30);
}

void reachDefault(){
    Ycoord = 150;
    Xcoord = 10;
    open = 0;
}

void reachTarget(size_t info){
  (void)info;
  int x, y, o;
  if (Wire.available() == 3){
    x = Wire.read();
    Serial.print(x);
    Serial.print(" ");

    y = Wire.read();
    Serial.print(y);
    Serial.print(" ");

    o = Wire.read();
    Serial.println(o);
    
    Ycoord = y;
    Xcoord = x;
    open = o;
  }

  
}
