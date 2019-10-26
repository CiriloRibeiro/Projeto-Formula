/************************************************************************************
 *   
 *  Name    : MMA8453_n0m1 Library Example: DataMode                       
 *  Author  : Noah Shibley, Michael Grant, NoMi Design Ltd. http://n0m1.com                       
 *  Date    : Feb 10th 2012                                    
 *  Version : 0.1                                              
 *  Notes   : Arduino Library for use with the Freescale MMA8453Q via i2c. 
 *
 ***********************************************************************************/

#include <Wire.h>
#include <MMA8453_n0m1.h>

unsigned long timer = 0;
long loopTime = 5000; 


MMA8453_n0m1 accel;

void setup()
{
  Serial1.begin(57600); 
  timer = micros();
  accel.setI2CAddr(0x1C); //change your device address if necessary, default is 0x1C
  accel.dataMode(true, 4); //enable highRes 10bit, 2g range [2g,4g,8g]
}

void loop()
{
  timeSync(loopTime);
  float x = accel.x() - 6 ;
  float y = accel.y() + 17;
  float z = accel.z() -130;
  accel.update();
  sendToGui(&x, &y, &z);
 /* Serial.print("x: ");
  Serial.print(accel.x()/125);
  Serial.print ("g");
  Serial.print(" y: ");
  Serial.print(accel.y()/125);
  Serial.print ("g");
  Serial.print(" z: ");
  Serial.print(accel.z()/125);
  Serial.println ("g"); */

  /*  Serial.print("x: ");
  Serial.print(accel.x());
  Serial.print(" y: ");
  Serial.print(accel.y());
  Serial.print(" z: ");
  Serial.print(accel.z());*/

}

void timeSync(unsigned long deltaT){
  unsigned long currentTime = micros();
  long timeToDelay = deltaT - (currentTime - timer);
  if (timeToDelay >= 5000){
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0){
    delayMicroseconds(timeToDelay);
  }
  timer = currentTime + timeToDelay;
}

void sendToGui(float* data1, float* data2, float* data3){
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte buf[12] = {byteData1[0], byteData1[1], byteData1[2], byteData1[3],
                 byteData2[0], byteData2[1], byteData2[2], byteData2[3], 
                 byteData3[0], byteData3[1], byteData3[2], byteData3[3]};
  Serial.write(buf, 12);
}
