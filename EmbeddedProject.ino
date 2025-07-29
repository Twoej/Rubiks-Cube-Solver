#include <AccelStepper.h>
#include <LiquidCrystal_I2C.h>

//Initialize
#define stepPin1 5        //LSB for step bit pattern
#define dirPin1 2         //LSB for dir bit pattern
#define inputPin1 8       //LSB for input bit pattern
#define dirSwitch 11      //Input for choosing direction of turn
#define bufferSwitch 12   //Input for buffering moves
#define stepEn 13         //Pin that enables the step decoder
#define dirEn A1          //Pin that enables the dir decoder

float speed = 20000;
float accel = 10000;
int moveDelay = 0;

char moveToExecute;
int prevInput = 7;

int currentUserSpeedInput = 959;

char buffer[20];

AccelStepper *motors[6];

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastLCDUpdateTime = 0;

//LCD state machine
bool LCDDefault = false;
bool LCDSpeed = false;
bool LCDInput = false;

//Method declarations
void moveMotor(char move);
int waitForInput();
int getInput();
char inputToMove(int input, bool counterClockwise);
void userChangeSpeed();
char *moveLCDFormat(char move);

void setup() {
  Serial.begin(9600);
  //Initializing pins
  for (int i = dirPin1; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
  for (int i = inputPin1; i < 11; i++) {
    pinMode(i, INPUT);
  }
  pinMode(dirSwitch, INPUT_PULLUP);
  pinMode(bufferSwitch, INPUT_PULLUP);
  pinMode(stepEn, OUTPUT);
  pinMode(dirEn, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);

  //Creating motor objects
  for (int i = 0; i < 6; i++) {
    motors[i] = new AccelStepper(1, stepPin1, dirPin1, stepEn, dirEn, 3, i);
    motors[i]->setMaxSpeed(speed);
    motors[i]->setSpeed(speed);
    motors[i]->setAcceleration(accel);
    motors[i]->setCurrentPosition(0);
  }

  //Initializing LCD
  lcd.init();
  lcd.backlight();
  lcd.print("Input a move");

  //Getting initial speed
  userChangeSpeed();
  LCDSpeed = false;
}

void loop() {
    if (Serial.available() > 0) {
      while (true) {
        bool LCDRead = false;
        bool LCDError = false;
        bool LCDSolve = false;
        if (Serial.available() > 0){
          String piSer = Serial.readStringUntil('\n');
          if (piSer == "moves") {
            executePiMoves(LCDSolve);
          } else if (piSer =="complete") {
            break;
          } else if (piSer == "read") {
            lcd.clear();
            LCDRead = true;
            LCDDefault = false;
            lcd.setCursor(0, 0);
            lcd.print("Reading Cube");
            lastLCDUpdateTime = millis();
            Serial.println("updated");
          } else if (piSer == "error-detect") {
            lcd.clear();
            LCDRead = false;
            LCDError = true;
            lcd.setCursor(0, 0);
            lcd.print("Resolving");
            lcd.setCursor(0, 1);
            lcd.print("Discrepancies");
            lastLCDUpdateTime = millis();
            Serial.println("updated");
          } else if (piSer == "solve") {
            lcd.clear();
            LCDError = false;
            LCDSolve = true;
            lcd.setCursor(0, 0);
            lcd.print("Solving!");
            lastLCDUpdateTime = millis();
            Serial.println("updated");
          }
        }
      }
    }
  //Variables that reset every loop
  bool bufferUsed = false;
  int bufferCount = 0;
  int inputBuffer;
  bool counterClockwise;
  bool bufferFull = false;
  //While the move buffer is switched on
  while (digitalRead(bufferSwitch) == LOW) {
    //If the number of input moves is less than 20
    if (bufferCount < 20) {
      //Wait for a move
      inputBuffer = waitForInput();
      if (inputBuffer == -1) {    //This triggers when the buffer switch is turned off
        break;
      }
      prevInput = inputBuffer;    //This is used in waitForInput() to ensure there are no repeat inputs when pressing once
      //If direction switch is counterclockwise
      if (digitalRead(dirSwitch) == HIGH) {
        counterClockwise = false;
      } else {
        counterClockwise = true;
      }
      //Add move to buffer
      char moveAsChar = inputToMove(inputBuffer, counterClockwise);
      buffer[bufferCount] = moveAsChar;
      //Set LCD to display move
      lcd.setCursor(0, 0);
      lcd.print("Move added to");
      lcd.setCursor(0, 1);
      lcd.print("buffer:     ");
      char *formattedMove = moveLCDFormat(moveAsChar);    //Formats the move to standard Rubik's move string
      lcd.setCursor(10, 1);
      lcd.print(formattedMove[0]);
      lcd.print(formattedMove[1]);
      free(formattedMove);
      lastLCDUpdateTime = millis();
      LCDDefault = false;
      LCDSpeed = false;

      bufferCount++;
    } else {
      //If the number of input moves is 20
      if (bufferFull == false) {
        //Indicate that the buffer is full to user on LCD display
        lcd.clear();
        lcd.setCursor(5, 0);
        lcd.print("Buffer");
        lcd.setCursor(6, 1);
        lcd.print("Full!");
        bufferFull = true;
      }
    }
  }

  if (bufferCount > 0) {
    //Clear LCD if buffer was used
    lcd.clear();
  }

  int bufferCountMax = bufferCount;   //Used to get the first move in the array
  //While the move buffer has moves
  while (bufferCount > 0) {
    //Speed can be changed during execution, so this allows the speed control on the LCD
    //to be overwritten if it has been 2 seconds plus the move delay
    if ((millis() - lastLCDUpdateTime) >= (2000 + moveDelay) && LCDSpeed) {
      LCDSpeed = false;
      lcd.clear();
    }
    //If the speed control is not on the LCD
    if (!LCDSpeed) {
      //Set the currently executing move to display on the LCD
      lcd.setCursor(0, 0);
      lcd.print("Current move:");
      lcd.setCursor(8, 1);
      lcd.print("  ");
      lcd.setCursor(8, 1);
      char *formattedMove = moveLCDFormat(buffer[bufferCountMax - bufferCount]);    //Formats the move to standard Rubik's move string
      lcd.print(formattedMove[0]);
      lcd.print(formattedMove[1]);
      free(formattedMove);
      lastLCDUpdateTime = millis();
    }

    //Adjust speed to user selection
    userChangeSpeed();
    //Execute the indexed move
    moveMotor(buffer[bufferCountMax - bufferCount]);
    //Iterate to the next move
    bufferCount--;
    //Delay a time based on the speed set by user
    delay(moveDelay);
    //On the last execution, set values to indicate current state
    if (bufferCount == 1) {
      prevInput = 7;
      lastLCDUpdateTime = millis();
      LCDDefault = false;
    }
  }

  //Clear move buffer
  for (int i = 0; i < 20; i++) {
    buffer[i] = NULL;
  }

  //Adjust speed to user selection
  userChangeSpeed();
  //Get user input
  int input = getInput();
  //Check if there is new user input
  if (input != 7 && input != prevInput) {   //7 is the bit pattern for no input
  //Check if clockwise switch is flipped or not
    if (digitalRead(dirSwitch) == HIGH) {
      counterClockwise = false;
    } else {
      counterClockwise = true;
    }
    moveToExecute = inputToMove(input, counterClockwise);
    //If the top line of the LCD is not already in the
    //appropriate format, print the topline to indicate the
    //current move
    if (!LCDInput) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Current move:");
    }
    //Update bottom of lCD with currently pressed move
    lcd.setCursor(8, 1);
    lcd.print("  ");      //Clear previous move so even if move is the same it will flash
    lcd.setCursor(8, 1);
    char *formattedMove = moveLCDFormat(moveToExecute);   //Formats the move to standard Rubik's move string
    lcd.print(formattedMove[0]);
    lcd.print(formattedMove[1]);
    free(formattedMove);
    LCDInput = true;
    LCDDefault = false;
    LCDSpeed = false;
    lastLCDUpdateTime = millis();

    //Move motor indicated by selected move
    moveMotor(moveToExecute);
  }

  //Store the the input to ensure that one button press does not trigger multiple
  if (input != prevInput) {
    prevInput = input;
  }

  //If the LCD has not been updated in 2 seconds plus the move delay (and LCD is not default state)
  if ((millis() - lastLCDUpdateTime) >= (2000 + moveDelay) && !LCDDefault) {
    //Set LCD to its default state
    LCDDefault = true;
    LCDSpeed = false;
    LCDInput = false;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Input a move");
  }
}

/*
void moveMotor()
This function takes a move in the format of u, d, l, r, f, b for counterClockwise or U, D, L, R, F, B
for clockwise. It then determines which motor this move corrosponds to and if it should
be clockwise or counterclockwise. It then sets the speed and acceleration for the motor and steps
the motor 100 steps in the appropriate direction.
Parameters: char move
Returns: nothing
*/
void moveMotor(char move) {
  int motor;

  bool counterClockwise = true;

  //Determine which motor should execute the move (which face), and the direction
  switch (move) {
    case 'u':
      motor = 0;
      break;
    case 'U':
      motor = 0;
      counterClockwise = false;
      break;
    case 'd':
      motor = 1;
      break;
    case 'D':
      motor = 1;
      counterClockwise = false;
      break;
    case 'l':
      motor = 2;
      break;
    case 'L':
      motor = 2;
      counterClockwise = false;
      break;
    case 'r':
      motor = 3;
      break;
    case 'R':
      motor = 3;
      counterClockwise = false;
      break;
    case 'f':
      motor = 4;
      break;
    case 'F':
      motor = 4;
      counterClockwise = false;
      break;
    case 'b':
      motor = 5;
      break;
    case 'B':
      motor = 5;
      counterClockwise = false;
      break;
    default:
      return;
  }
  //Set the speed and acceleration for this motor based on the stored user selection
  motors[motor]->setSpeed(speed);
  motors[motor]->setAcceleration(accel);
  if (counterClockwise) {
    //If it is counterClockwise, move the motor 90 deg counterClockwise (100 steps)
    motors[motor]->move(100);
    motors[motor]->runToPosition();
  } else {
    //If it is clockwise, move the motor 90 deg clockwise (-100 steps)
    motors[motor]->move(-100);
    motors[motor]->runToPosition();
  }
}

/*
int waitForInput()
This function waits until the current input is different from the previous input. This is
to ensure that the current input is not a repeated input from the button being held. Once the
button is released, the function waits for an input indicating a button press. On this input it
will return the input. If at any point the buffer switch is turned off, the program returns
-1 so that the buffer can end without waiting for user input.
Parameters: none
Returns: Integer indicating input state
*/
int waitForInput() {
  //Waits for user to release button
  while (getInput() == prevInput) {
    delay(100);
  }
  //Waits for user to press new button
  while (getInput() == 7) {
    userChangeSpeed();
    delay(100);
    //If user turns off input buffer, there is no need to return an input
    //so return -1
    if (digitalRead(bufferSwitch) == HIGH) {
      return -1;
    }
  }
  return getInput();
}

/*
int getInput()
This function creates an array of 3 integers (one for each bit of the input multiplexer),
then it checks each of the input pins 100 times recording the amount of times each of them
was high. For each of the three that read high for half of these times, set their bit to 1
in the input variable. The input variable now represents the bit pattern of the currently
presed button (excluding key bounce).
Parameters: none
Returns: Integer indicating input state
*/
int getInput() {
  int debounce[3] = {0, 0, 0};
  int input = 0;
  //Checks for 100 inputs to determine input state
  for (int i = 0; i < 100; i++) {
    for (int j = 0; j < 3; j++) {
      if (digitalRead(j + 8) == HIGH) {
        debounce[j] += 1;
      }
    }
  }
  //If the input state is the same over half the time (remove bounce)
  for (int i = 0; i < 3; i ++) {
    if (debounce[i] > 50)
      //Add the bit in the right location by bitshifting it
      input += 1 << i;
  }
  return input;
}

/*
char inputToMove(int input, bool counterClockwise)
This function takes in the current input represented by an integer and the state of the clockwise
switch and converts it to one output character to be read by the moveMotor function. This functionality
could be integrated into the moveMotor function but having a separate funtion makes it more readable and 
modular.
Parameters: int input, bool counterClockwise
Returns: Character representing inputted move
*/
char inputToMove(int input, bool counterClockwise) {
  char moveChar;
  switch (input) {
    case 0:
      if (counterClockwise) {
        moveChar = 'b';
      } else {
        moveChar = 'B';
      }
      break;
    case 1:
      if (counterClockwise) {
        moveChar = 'f';
      } else {
        moveChar = 'F';
      }
      break;
    case 2:
      if (counterClockwise) {
        moveChar = 'r';
      } else {
        moveChar = 'R';
      }
      break;
    case 3:
      if (counterClockwise) {
        moveChar = 'l';
      } else {
        moveChar = 'L';
      }
      break;
    case 4:
      if (counterClockwise) {
        moveChar = 'd';
      } else {
        moveChar = 'D';
      }
      break;
    case 5:
      if (counterClockwise) {
        moveChar = 'u';
      } else {
        moveChar = 'U';
      }
      break;
  }
  return moveChar;
}

/*
void userChangeSpeed()
This function reads the user input by reading the voltage at a voltage divider consisting of
a 10k potentiomter and a 1k resistor. It only adjusts the speed if the input has changed by 30 (147 mV).
This is to remove the noise created by the motor power supply. There is linear functions casting the voltage
reading to speed, acceleration, and move delay. Speed ranges from about 400 to 20000 steps per second, accleration
ranges from 200 to 10000 steps per second^2, and move delay ranges from 500 ms to 0 ms. The function also displays
the speed change on the LCD display.
Parameters: none
Returns: none
*/
void userChangeSpeed() {
  //Take in the user input
  int userInput = analogRead(A0);
  //Check if desired speed has changed
  if (abs(userInput - currentUserSpeedInput) > 30) {
    //Function for new speed value from user input
    speed = (22.659 * userInput) - 1729.95;
    //Acceleration should be half of speed
    accel = speed / 2;
    //Function for new delay value from user input
    moveDelay = (int)((-0.57803 * userInput) + 554.331);
    //Ensures that moveDelay is not negative as negative time is impossible
    if (moveDelay < 0) {
      moveDelay = 0;
    }
    //Saves the current input for comparison later
    currentUserSpeedInput = userInput;

    //If the speed menu is not already on the LCD, change the first line
    //formatting to the speed menu
    if (!LCDSpeed) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Speed: ");
    }
    //Print the speed as a percent of the max voltage
    lcd.setCursor(7, 1);
    lcd.print((int)(((float)(userInput) / 1020.0) * 100));
    lcd.print(" % ");
    //Set the LCD state
    lastLCDUpdateTime = millis();
    LCDSpeed = true;
    LCDDefault = false;
    LCDInput = false;
  }
}

/*
char *moveLCDFormat(char move)
This function takes a move character in the internal format (u, d, l, r, f, b,
U, D, L, R, F, B) and converts it to a character array in the standard Rubik's move
format (U', D', L', R', F', B', U, D, L, R, F, B).
Parameters: char move
Returns: Pointer to a character array containing the formatted move
*/
char *moveLCDFormat(char move) {
  //Create a pointer to a character array
  static char formattedMove[2];
  //If the move is lowercase (counterclockwise)
  if (islower(move)) {
    //Make the first character uppercase move
    formattedMove[0] = toupper(move);
    //Set the second character to the counterclockwise symbol (')
    formattedMove[1] = 39;
  } else {
    //If the move is uppcase (clockwise)
    //Set the first character to the move
    formattedMove[0] = move;
    //Set the second character to an empty space to remove any garbage at the memory location
    formattedMove[1] = ' ';
  }
  return formattedMove;
}

void executePiMoves(bool solving) {
  Serial.println("ready");
  String piSer;
  char piBuffer[60];
  int piBufferIndex = 0;
  while (true) {
    userChangeSpeed();
    if (Serial.available() > 0) {
      piSer = Serial.readStringUntil('\n');
      if (piSer == "stop") {
        break;
      }
      piBuffer[piBufferIndex] = piSer[0];
      piBufferIndex++;
      Serial.println("next");
    }
    delay(1);
  }
  for (int i = 0; i < piBufferIndex; i++) {
    if (solving) {
      lcd.setCursor(10, 1);
      char *formattedMove = moveLCDFormat(piBuffer[i]);    //Formats the move to standard Rubik's move string
      lcd.print(formattedMove[0]);
      lcd.print(formattedMove[1]);
      free(formattedMove);
      lastLCDUpdateTime = millis();
    }
    moveMotor(piBuffer[i]);
    delay(moveDelay);
  }
  Serial.println("done");
}
