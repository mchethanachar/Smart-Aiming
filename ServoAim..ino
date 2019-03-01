/*
Written by:Chethan M
           BMS College of Engineering
           Bangalore
           mchethan.achar@gmail.com
Last modified:20th Nov 2018
*/
/*
 * This code recieves the angle from the python script 
 * angle btw(including) 0 and 179 is for horizontle servo motor
 * angle btw(including) 180 and 360 is for vertical servo motor
 */
#include <Servo.h> 
 
Servo myservo;  
Servo myservo2;               
 
int pos = 0;
int servodata,prev,prev2;

void setup()  {
  Serial.begin(9600);  
  myservo.attach(9);
  myservo2.attach(10);
  myservo.write(90);
  delay(100);
  myservo2.write(90);
  delay(100);
  prev=0;
  prev2=0;
}

void loop()   
{
  if (Serial.available() > 0)
  {
   servodata = Serial.parseInt();
    if(servodata<180)
    {
    if(prev<servodata)
    {
      for(pos = prev; pos <= servodata; pos += 1)  
  {                                  
    myservo.write(pos);               
    Serial.flush();
    delay(1);          
  } 
    }
  else
  {
    for(pos = prev; pos >= servodata; pos -= 1)   
  {                                  
    myservo.write(pos);               
    Serial.flush();
    delay(1);         
  } 
  }
  prev=servodata;
    }
    else
    {
      servodata=servodata-180;
      if(prev2<servodata)
    {
      for(pos = prev2; pos <= servodata; pos += 1)  
  {                                   
    myservo2.write(pos);               
    Serial.flush();
    delay(1);         
  } 
    }
  else
  {
    for(pos = prev2; pos >= servodata; pos -= 1)   
  {                                   
    myservo2.write(pos);               
    Serial.flush();
    delay(1);         
  } 
  }
  prev2=servodata;
    }
  }
}


