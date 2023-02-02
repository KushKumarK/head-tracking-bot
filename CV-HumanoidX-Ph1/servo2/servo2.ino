#include <Servo.h>

int inbyte;
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position
int pre= 90;

void setup() {
  Serial.begin(9600);
  myservo.attach(11);  // attaches the servo on pin 9 to the servo object
  myservo.write(90);
}

void loop() {

  if(Serial.available()>0){
    inbyte=Serial.parseInt();
    Serial.println(pos);
    if(inbyte>0){
      pos = pos+10;
      if(pos>180){
        pos=180;
      }
      for (int i = pre; i <= pos; i ++) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(i);              // tell servo to go to position in variable 'pos'        
        delay(5);                       // waits 15ms for the servo to reach the position
      }
    }
    if(inbyte==0){
      myservo.write(pre);
    }
    if(inbyte<0){
      pos = pos-10;
      if(pos<0){
        pos=0;
      }
      for (int i = pre; i >= pos; i --) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(i);              // tell servo to go to position in variable 'pos'        
        delay(5);                       // waits 15ms for the servo to reach the position
      }
    }
    
      pre=pos;
   }
  }
