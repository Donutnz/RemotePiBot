//Pi bot control. Camera X/Y and motors.

#include <Servo.h>

Servo srvoX;
Servo srvoY;
int Rmotor=3;
int Lmotor=5;

void setup() {
  pinMode(Rmotor,OUTPUT);
  pinMode(Lmotor,OUTPUT);
  srvoX.attach(9);
  srvoY.attach(10);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Ready to receive!\nMotors (0-245):\nL = Left motor\nR = Right motor\nCamera (1-179):\nX = X axis\nY = Y axis\n");
}

void loop() {
  if(Serial.available()>0){
    byte inp[4];
    String pos;
    int val;
    char ind;
    Serial.readBytes(inp,4);
    ind=inp[0];
    for(int y=1;y<4;y++){
      pos+=inp[y]-'0';
    }
    val=pos.toInt();
    Serial.print(ind);
    Serial.println("Val: "+String(val));
    /*
    byte rawdata[2];
    Serial.readBytes(rawdata,2);
    char ind=char(rawdata[0]);
    int val=int(rawdata[1]);
    Serial.println("Got passed: "+String(rawdata[0]));
    
      char ind=char(Serial.parseInt());
      int val=Serial.parseInt();
      Serial.println("Ind: "+ind);
      Serial.println("Val: "+String(val));
    */
    if(ind=='R'){
      analogWrite(Rmotor,val);
      Serial.println("Set right speed to: "+String(val));
    }
    else if(ind=='L'){
      analogWrite(Lmotor,val);
      Serial.println("Set left speed to: "+String(val));
    }
    else if(ind=='X'&&(val>0&&val<179)){
      srvoX.write(val);
      Serial.println("Cam X axis to: "+String(val));
      delay(2);
    }
    else if(ind=='Y'&&(val>0&&val<179)){
      srvoY.write(val);
      Serial.println("Cam Y axis to: "+String(val));
      delay(2);
    }
    else if(ind=='E'){
      srvoX.write(90);
      srvoY.write(90);
      analogWrite(Rmotor,0);
      analogWrite(Lmotor,0);
      Serial.println("All reset");
    }
    else{
      Serial.println("No correct indicator char found");
    }
  }
}



//Written by Donutnz
