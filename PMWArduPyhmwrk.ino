#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11

float tempC;
float tempF;
float humidity;
int potPin =A0;
int potVal;

int setupTime = 500;
int refreshrate = 500;

DHT TH(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
   TH.begin();
   delay(setupTime);
}

void loop() {
  // put your main code here, to run repeatedly:
  potVal=analogRead(potPin);
  tempC=TH.readTemperature();
  tempF=TH.readTemperature(true);
  humidity=TH.readHumidity();

  //Serial.print(tempF);
  //Serial.println(" Degrees F!");
  Serial.println("V");
  Serial.println(potVal);
  Serial.println("C");
  Serial.println(tempC);
  Serial.println("H");
  Serial.println(humidity);
  
  delay(refreshrate);

}
