#include <Servo.h>

#define Apin 9
#define Bpin 10
#define Cpin 11

#define control1 A0
#define control2 A1

#define lengthA 100
#define lengthB 100
#define lengthC 10

Servo servoA, servoB, servoC;

float theta1, theta2, theta3;
float thetadamp1, thetadamp2, thetadamp3;
float thetaprev1, thetaprev2, thetaprev3; 
int Xcoord = 100, Ycoord = 100;

int setpoint1 = 90, setpoint2 = 180;
float damping = 0.05;

void setup(){
  servoA.attach(Apin);
  servoB.attach(Bpin);
  servoC.attach(Cpin);
  pinMode(control1, INPUT_PULLUP);
  pinMode(control2, INPUT_PULLUP);

  servoA.write(setpoint1);
  servoB.write(setpoint2);
  servoC.write(setpoint1);

  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    Xcoord = Serial.parseInt();
    Ycoord = Serial.parseInt();

    if (Serial.peek() == '\n' || Serial.peek() == '\r'){
      Serial.read();
    }
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
  theta3 = setpoint1 - shiftC

  thetadamp1 = theta1 - thetaprev1;
  thetaprev1 = thetaprev1 + (thetadamp1 * damping);

  servoA.write(thetaprev1);
  delay(10);
  servoB.write(shiftB);
  delay(10);
  servoC.write(setpoint1 - shiftC);

  Serial.print("X =  ");
  Serial.print(Xcoord);
  Serial.print(" ,");
  Serial.print("Y =  ");
  Serial.print(Ynewcoord);
  Serial.print(" -- ");
  Serial.print(thetaprev1);
  Serial.print(" -- ");
  Serial.print(theta2);
  Serial.print(" -- ");
  Serial.print(theta3);
  Serial.println(" .");
  delay(10);
}
