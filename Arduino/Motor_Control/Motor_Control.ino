int L298N_IN1 = 6; //Right Side Forward
int L298N_IN2 = 9; //Right Side Backwards

int L298N_IN3 = 10; //Left Side Forward
int L298N_IN4 = 11; //Left Side Backwards

String readString = "005 005";

void setup() {
  // open the serial port at 9600 bps:
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(L298N_IN1, OUTPUT);
  pinMode(L298N_IN2, OUTPUT);
  pinMode(L298N_IN3, OUTPUT);
  pinMode(L298N_IN4, OUTPUT);

  analogWrite(L298N_IN1, 0);
  analogWrite(L298N_IN4, 0);
  analogWrite(L298N_IN2, 0);
  analogWrite(L298N_IN3, 0);

  Serial.println("setup completed");
}

void loop() {
  // put your main code here, to run repeatedly:
  String leftString;
  String rightString;
  int leftSpeed;
  int rightSpeed;
  int directionInt; //1 For forward, 0 for Backwards
  readString = "";

  while (Serial.available()) {
    delay(3);  //delay to allow buffer to fill
    if (Serial.available() > 0) {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    }
  }

  if (readString.length() > 0) {
    Serial.println(readString); //see what was received

    // expect a string like 0100-100 containing the two motor speeds
    leftString = readString.substring(0, 4); //get the first four characters
    rightString = readString.substring(4, 8); //get the next four characters

    Serial.println(leftString);  //print to serial monitor to see parsed results
    Serial.println(rightString);

    leftSpeed = leftString.toInt();
    rightSpeed = rightString.toInt();

    Serial.println("the numbers are :");
    Serial.println(leftSpeed);  //print to serial monitor to see number results
    Serial.println(rightSpeed);

    setLeftWheels(leftSpeed);
    setRightWheels(rightSpeed);
  }


}

void setLeftWheels(int val)
{
  val = val * 2.55;
  
  if(val >= 0)
  {
    analogWrite(L298N_IN4, 0);
    analogWrite(L298N_IN3, val);
  }
  else
  {
    analogWrite(L298N_IN3, 0);
    analogWrite(L298N_IN4, abs(val));
  }
}

void setRightWheels(int val)
{
  val = val * 2.55;
  
  if(val >= 0)
  {
    analogWrite(L298N_IN1, val);
    analogWrite(L298N_IN2, 0);
  }
  else
  {
    analogWrite(L298N_IN2, abs(val));
    analogWrite(L298N_IN1, 0);
  }

}

