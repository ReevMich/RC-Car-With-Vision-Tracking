///////////////////////////////////////////////////////////////////////
// Author(s): Michael Reeves
// File: LCD_Display_Code.ino
// Description: License Plate Generator
///////////////////////////////////////////////////////////////////////

// include the library code:
#include <LiquidCrystal.h>
#include <Wire.h>
 
#define REDLITE 3
#define GREENLITE 5
#define BLUELITE 6
#define NUM_OF_TERMS 13

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// List of phrases or words for row 1
String line1[NUM_OF_TERMS] =  { "   MY NAME IS   ", "     I LOVE     ", "      CPSC      ", 
"     Give me    ", "    #TEAMTUX    ", "  Raspberry Pi  ", " SAY HELLO TO MY ", "    UNIX IS     ", "    ALL HAIL    ", "  TEAM ONE IS   ", "   CHUY WALTER  ", 
"   CHUY-JESUS  ", "  WALLIE-WALTER "};

// List of phrases or words for row 2
String line2[NUM_OF_TERMS] = { "CUTIE PANTS 3000", "    #TEAMTUX    ", "      434       ",  
"    the Green   ", "    #TEAMTUX    ", " is no Ardunio  " ,"  little friend ", "    THE BEST    ", "    THE TUX     ", "   BEST TEAM!   ", "  MICHAEL JOSH  ", 
"CAPTAIN-MICHAEL", "  JOSHUA-JOSH  "};

// you can change the overall brightness by range 0 <---> 255
int brightness = 255;

 // init setup
void setup() {
  // set up the LCD's number of rows and columns: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  getNewWord();
  
  pinMode(REDLITE, OUTPUT);
  pinMode(GREENLITE, OUTPUT);
  pinMode(BLUELITE, OUTPUT);

  brightness = 255;
}
 
// Loop
void loop() {
  getNewWord();
  colorCylceLoop();
}

// Pleases the newly generated word on the display
void getNewWord(){
  lcd.clear();
  
  int randNumber = random(0,NUM_OF_TERMS);

  lcd.setCursor(0,0);
  line1[randNumber].toUpperCase();
  lcd.print(line1[randNumber]);
  lcd.setCursor(0,1);
  line2[randNumber].toUpperCase();
  lcd.print(line2[randNumber]);
}

/* Loop through all the colors  */
void colorCylceLoop(){

  int r = random(0, 256); 
  int g = random(0,256);
  int b = random(0,256);

  setBacklight(r-1,g-1,b-1);
  delay(3000);
}

 /*
 * All code below this is all from adafruit
 * 
 */
 
void setBacklight(uint8_t r, uint8_t g, uint8_t b) {
  // normalize the red LED - its brighter than the rest!
  r = map(r, 0, 255, 0, 100);
  g = map(g, 0, 255, 0, 150);
 
  r = map(r, 0, 255, 0, brightness);
  g = map(g, 0, 255, 0, brightness);
  b = map(b, 0, 255, 0, brightness);
 
  // common anode so invert!
  r = map(r, 0, 255, 255, 0);
  g = map(g, 0, 255, 255, 0);
  b = map(b, 0, 255, 255, 0);
  Serial.print(" R = "); Serial.print(r, DEC);
  Serial.print(" G = "); Serial.print(g, DEC);
  Serial.print(" B = "); Serial.println(b, DEC);
  analogWrite(REDLITE, r);
  analogWrite(GREENLITE, g);
  analogWrite(BLUELITE, b);
}


