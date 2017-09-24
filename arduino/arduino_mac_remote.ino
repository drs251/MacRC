// Include IRLib decode base
#include <IRLibDecodeBase.h>
#include <IRLibRecvPCI.h>
// Include the protocol (in this case Philipps RC5)
// This depends on the remote control and the receiver module
#include <IRLib_P03_RC5.h>

IRdecodeRC5 myDecoder;

//pin number for the receiver signal pin:
IRrecvPCI myReceiver(2);
const int groundPin = 3;
// use an IO pin to supply the receiver with power:
const int inputVoltagePin = 4;

bool lastToggleBit;
int lastCommand;


void setup() {
  lastToggleBit = 0;
  lastCommand = -1;
  pinMode(groundPin, OUTPUT);
  digitalWrite(groundPin, LOW);
  pinMode(inputVoltagePin, OUTPUT);
  digitalWrite(inputVoltagePin, HIGH);
  Serial.begin(9600);
  myReceiver.enableIRIn();
}


void loop() {
  //Continue looping until you get a complete signal received
  if (myReceiver.getResults()) { 
    myDecoder.decode();
    if (myDecoder.value != 0) {
      bool toggleBit = (0b0100000000000 & myDecoder.value) != 0;
      int command = 0b0000000111111 & myDecoder.value;
      if (toggleBit != lastToggleBit || command != lastCommand) {
        //Serial.println(command);
        switch (command) {
          case 16:
            // louder
            Serial.println("L");
            break;
          case 17:
            // softer
            Serial.println("S");
            break;
          case 13:
            // mute
            Serial.println("M");
            break;
          case 32:
            // next track
            Serial.println("N");
            break;
          case 33:
            // previous track
            Serial.println("B");
            break;
          case 50:
            // play
            Serial.println("P");
            break;
          case 54:
            // pause
            Serial.println("H");
            break;
        }
        lastToggleBit = toggleBit;
        lastCommand = command;
      }
    }
    //Restart receiver
    myReceiver.enableIRIn();
  }
}

