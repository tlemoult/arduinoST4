/*
    Generate impultion on 4 directions for ST4 Telescope input
    Serial Port @ 9600 baud. Syntax:
      N234\n
      E231\n
      W345\n
      S352\n
 */

String inputString = "";         // a string to hold incoming data
int     inputStringLen=0;         // len of input String
boolean stringComplete = false;  // whether the string is complete

//Rel1-> pin4
//Rel2 -> pin 7
//Rel3 -> pin 8
//Rel4 -> pin 12
#define PIN_WEST 4
#define PIN_NORTH 7
#define PIN_EST 8
#define PIN_SOUTH 12

void setup() {
  // initialize serial:
  Serial.begin(9600);

  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  inputString= "";

  // initialize the digital pin as an output.

  pinMode(PIN_WEST, OUTPUT);     
  digitalWrite(PIN_WEST,LOW);  
  pinMode(PIN_NORTH, OUTPUT);     
  digitalWrite(PIN_NORTH,LOW);  
  pinMode(PIN_EST, OUTPUT);     
  digitalWrite(PIN_EST,LOW);  
  pinMode(PIN_SOUTH, OUTPUT);     
  digitalWrite(PIN_SOUTH,LOW);  

  Serial.print("HelloSetup\n");
}

int parseDelayValue() {
  String delayString = "";
  int i;
  for (i=0;i<inputStringLen;i++) {
    if (isDigit(inputString[i])) {
      delayString += inputString[i];
    }
  }

  i=delayString.toInt();
  // scrap bad value.
  if (i>=0 && i<30000) 
    { return i; }
  else
    { return 0; }
}

void loop() {

  int pulseDuration=200;

  if (stringComplete) {
    int len = inputString.length();

    switch (inputString[0]) {

//deplacement libre
      case 'n':
        digitalWrite(PIN_EST,LOW);
        digitalWrite(PIN_WEST,LOW);
        digitalWrite(PIN_SOUTH,LOW);
        digitalWrite(PIN_NORTH,HIGH);
        break;

      case 'e':
        digitalWrite(PIN_NORTH,LOW);
        digitalWrite(PIN_WEST,LOW);
        digitalWrite(PIN_SOUTH,LOW);
        digitalWrite(PIN_EST,HIGH);
        break;

      case 'w':
        digitalWrite(PIN_NORTH,LOW);
        digitalWrite(PIN_EST,LOW);
        digitalWrite(PIN_SOUTH,LOW);
        digitalWrite(PIN_WEST,HIGH);
        break;

      case 's':
        digitalWrite(PIN_NORTH,LOW);
        digitalWrite(PIN_EST,LOW);
        digitalWrite(PIN_WEST,LOW);
        digitalWrite(PIN_SOUTH,HIGH);
        break;

// move stop
      case 'T':
        digitalWrite(PIN_NORTH,LOW);
        digitalWrite(PIN_EST,LOW);
        digitalWrite(PIN_WEST,LOW);
        digitalWrite(PIN_SOUTH,LOW);
        break;


// deplacement avec duree
      case 'N':
        digitalWrite(PIN_NORTH,HIGH);
        delay(parseDelayValue());
        digitalWrite(PIN_NORTH,LOW);
        break;

      case 'E':
        digitalWrite(PIN_EST,HIGH);
        delay(parseDelayValue());
        digitalWrite(PIN_EST,LOW);
        break;


      case 'W':
        digitalWrite(PIN_WEST,HIGH);
        delay(parseDelayValue());
        digitalWrite(PIN_WEST,LOW);
        break;

    
      case 'S':
        digitalWrite(PIN_SOUTH,HIGH);
        delay(parseDelayValue());
        digitalWrite(PIN_SOUTH,LOW);
        break;

    }

    inputString = "";
    inputStringLen=0;

    stringComplete = false;
  }
  
   

}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    inputStringLen +=1;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


