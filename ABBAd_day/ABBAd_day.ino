#include <SD.h> 
#define SD_ChipSelectPin 4   // using digital pin 4 as ChipSelect
#include <TMRpcm.h>          // audio playing library
 
/////////////////////////////////////////////
// SD card attached as follows: //
// ** MOSI - pin 11                        //
// ** MISO - pin 12                        //
// ** CLK  - pin 13                        //
// ** CS   - pin 4                         //
//                                         //
// ** Speaker - pin 9                      //
//                                         //
// ** LDR - pin A0                         //
/////////////////////////////////////////////
 
 
// declare global variables //

// create an TMRpcm object
TMRpcm audio;

// variables for picking a random file
char* fileName;
char *fileArray[26];
int arrSize = 26;

// LDR input
int sensorPin = A0;
int sensorValue = 0;

void setup() {
      
    // only need this if printing to serial monitor
    Serial.begin(9600);
    
    // need this so that subsequent calls to random() give different values
    // every time the sketch is executed (per Arduino docs)
    randomSeed(analogRead(1));
     
    // set audio output pin
    audio.speakerPin = 9;
  
    // see if the card is present and can be initialized:
    if (!SD.begin(SD_ChipSelectPin)) {  
        Serial.println("Cannot initialize SD card");
        return;   // don't do anything more if not
    }
    
    // set audio volume (0-7)
    audio.setVolume(3);
  
    // populate file name array
    makeFileArray(); 
}

void playRandom() {
    // select a random file and play it
    //Serial.println("About to get file to play...");
    fileName = getFileName();
    audio.play(fileName);
}

char* getFileName() {
    // get a random number and return the file name at that location in array
    int i = random(0, arrSize);
    return fileArray[i]; 
}


void loop() {  
  
    sensorValue = analogRead(sensorPin);  
    Serial.println(sensorValue);
 
    if ( sensorValue >= 650 ) {
        if ( !audio.isPlaying() ) {
            playRandom();
        }
    }
    else
        audio.stopPlayback();
   
    // wait 200ms so it's not constantly calling playRandom() when a bunch
    // of values are fluctuating around 800
    delay(200); 
}
