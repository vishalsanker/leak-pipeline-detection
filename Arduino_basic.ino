int X;
int Y;
float TIME = 0;
float FREQUENCY = 0;
float WATER1 = 0;
float WATER2 = 0;
float TOTAL = 0;

const int input1 = A0;
const int input2 = A1;
int temp = 0;

#include "HX711.h"
long psi1;
long psi2;
const int DOUT_PIN_1 = 2;
const int SCK_PIN_1 = 3; 

int relayPin = 10;
const int DOUT_PIN_2 = 6;
const int SCK_PIN_2 = 7; 

HX711 scale1;
HX711 scale2;

void setup() {
  Serial.begin(9600);
  pinMode(input1, INPUT);
  pinMode(input2, INPUT);
  pinMode(relayPin, OUTPUT);
  scale1.begin(DOUT_PIN_1, SCK_PIN_1);
  scale2.begin(DOUT_PIN_2, SCK_PIN_2);
  delay(2000);
}


void loop() {
  digitalWrite(relayPin, HIGH);
  X = pulseIn(input1, HIGH);
  Y = pulseIn(input1, LOW);
  TIME = X + Y;
  FREQUENCY = 1000000 / TIME;
  WATER1 = FREQUENCY / 7.5;
  

  if (FREQUENCY >= 0) {
    if (isinf(FREQUENCY)) {
      Serial.print("VOL. ; 0.00");
      Serial.print(" l/M ");
    } else {

      Serial.print("VOL. ; ");
      Serial.print(WATER1);
      Serial.print(" l/M ");
    }
  }
  
  X = pulseIn(input2, HIGH);
  Y = pulseIn(input2, LOW);
  TIME = X + Y;
  FREQUENCY = 1000000 / TIME;
  WATER2 = FREQUENCY / 7.5;
  

  if (FREQUENCY >= 0) {
    if (isinf(FREQUENCY)) {
      Serial.print("VOL. : 0.00");
      Serial.print(" L/M ");
    } else {

      Serial.print("VOL. : ");
      Serial.print(WATER2);
      Serial.print(" L/M ");
    }
  }
  delay(5000);
  if (WATER1 > WATER2 ){
    if(WATER1-WATER2 <= 1.00){
      temp += 1;
    }else{
      temp = 0;
    }
  }else{
    if(WATER2-WATER1 <= 1.00){
      temp += 1;
    }else{
      temp = 0;
    }
  }
  if (scale1.is_ready()) {
    long pressureValue1 = scale1.read();
    psi1 = pressureValue1 /415646 ;
    
  }
  
  if (scale2.is_ready()) {
    long pressureValue2 = scale2.read();
    psi2 = pressureValue2 /415646 ;
     
  }
  if (psi1>psi2){
    long diff = psi1 - psi2;
    Serial.print(" M ");
    Serial.print(diff);
    Serial.print(" K ");
  }else{
    long diff = psi2 - psi1;
    Serial.print(" M ");
    Serial.print(diff);
    Serial.print(" K ");
  }
  if (temp <= 5){
    digitalWrite(relayPin, LOW);
  }else{
    digitalWrite(relayPin, HIGH);
  }
  Serial.println(WATER1 - WATER2);
}
