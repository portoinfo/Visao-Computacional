#include <cvzone.h>

SerialData serialData(1,1); //(numOfValsRec,digitsPerValRec)
/*0 or 1 - 1 digit
0 to 99 -  2 digits
0 to 999 - 3 digits
 */
//SerialData serialData;   // if not receving only sending


int sendVals[2]; // min val of 2 even when sending 1
int valsRec[1];

int x = 0;

void setup() {

serialData.begin(9600);
pinMode(13,OUTPUT);
}

void loop() {

  // ------- To SEND --------
  x +=1;
  if (x==100){x=0;}
  sendVals[0] = x;
  serialData.Send(sendVals);

  // ------- To Recieve --------
  serialData.Get(valsRec);
  digitalWrite(13,valsRec[0]);

}