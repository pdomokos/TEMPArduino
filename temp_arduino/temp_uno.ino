#include <AM2302-Sensor.h>

constexpr unsigned int SENSOR_PIN {2U};
constexpr unsigned int SENSOR_PIN_2 {3U};
constexpr unsigned int PIR_SENSOR_PIN {4U};

AM2302::AM2302_Sensor am2302{SENSOR_PIN};
AM2302::AM2302_Sensor am2302_2{SENSOR_PIN_2};

//Thermometer with thermistor

/*thermistor parameters:
 * RT0:  10 000 Ω
 * B: 3977 K +- 0.75%
 * T0:  25 C
 * +- 5%
 */

//These  values are in the datasheet
#define RT0 10000   // Ω
#define B 3977      //  K
//--------------------------------------


#define VCC 5    //Supply  voltage
#define R 10000  //R=10KΩ

const long interval = 10000;
float RT, VR, ln, TX,  T0, VRT;

float readThermistor(int i);

void setup() {
   T0 = 25 + 273.15;                 //Temperature  T0 from datasheet, conversion from Celsius to kelvin

   Serial.begin(115200);
   while (!Serial) {
      yield();
   }

   am2302.begin();
   am2302_2.begin();
   delay(3000);

}

void loop() {
   auto status = am2302.read();
   auto status_2 = am2302_2.read();

   Serial.print("DHT1_T:");
   Serial.print(am2302.get_Temperature());
   Serial.print("#");
   Serial.print("DHT1_H:");
   Serial.print(am2302.get_Humidity());
   Serial.print("#");

   Serial.print("DHT2_T:");
   Serial.print(am2302_2.get_Temperature());
   Serial.print("#");
   Serial.print("DHT2_H:");
   Serial.print(am2302_2.get_Humidity());
   Serial.print("#");

   Serial.print("T1:");
   Serial.print(readThermistor(1));
   Serial.print("#");

   Serial.print("T2:");
   Serial.print(readThermistor(2));
   Serial.print("#");

   Serial.print("PIR1:");
   Serial.print(readPirSensor());
   Serial.println();
}

int readPirSensor(){
  int motionDetected = 0;  

  unsigned long startMillis = millis();  

  while (millis() - startMillis < interval) {

    if (digitalRead(PIR_SENSOR_PIN) == HIGH) {
      motionDetected = 1;
    }

  }

  return motionDetected;
}

float readThermistor(int i) {
  if(i==1){
    VRT = analogRead(A0);
  }else if(i==2){
    VRT = analogRead(A1);
  }              //Acquisition analog value of VRT
  VRT  = (5.00 / 1023.00) * VRT;      //Conversion to voltage
  VR = VCC - VRT;
  RT = VRT / (VR / R);               //Resistance of RT

  ln = log(RT / RT0);
  TX = (1 / ((ln / B) + (1 / T0))); //Temperature from thermistor

  TX =  TX - 273.15;                 //Conversion to Celsius

  return TX;

}