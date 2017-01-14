

// For the Thermistor: Attach VCC to left leg, an AnalogRead capable pin (2) to right leg  
// with a 10K resistor to GND in series. 
// For the Temp Sensor: Attach VCC to the left leg, an AnalogRead capable pin (6) to the 
// middle leg, and GND to the right leg. The letters and flat face should be facing you.  
// Check the datasheet if you want to verify the correct pin connections. 
// This example uses pin 2 and 6 on your LaunchPad, but can be changed to any analog pin.
// WARNING: the LM19 will get very hot to the touch if you have it plugged in backwards!

/* In the setup function we will initialize the Serial library
 * which let's us send and receive data over the UART channel
 */

#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <float.h>

#define DATA		0


/* In the loop section we will take measurements from our two sensors
 * perform any mathematical formulas to convert to the temperature,
 * and then print out the information to the console (serial monitor).
 */
void loop()
{
  // >>> Thermistor Section <<<
  // take in analog data from thermistor and run it through formulas 
  // and conversions
  
  float ThermistorVal = digitalRead(DATA);
  float ThermistorTempC;
  float ThermistorTempF;
 
 ThermistorTempC = logf(10000.0 * ((1024.0 / ThermistorVal - 1)));
           = logf(10000.0 / (1024.0 / ThermistorVal - 1)); // for pull-up configuration
 

/*
  Serial.print("Thermistor: ");
  Serial.print("vin=");
  Serial.print(ThermistorVal);
  Serial.print(" ");
  Serial.print("TempC=");
  Serial.print(ThermistorTempC);
  Serial.print("  ");
  Serial.print("TempF=");
  Serial.print(ThermistorTempF);
  Serial.println();

*/

printf("Temperature = %.1f C (%.1f F)\n", ThermistorTempC, ThermistorTempF);
  
  // >>> End of Thermistor Section <<<
  
  // >>> LM19 Section <<<
  // take in analog data from LM19 temp sensor and run it through
  // formulas and conversions
  
  // multiply analog read by VCC which is 3.3V on LaunchPad
  // divide that result by ADC range (256 for 8 bit, 1024 for 10 bit, 
  // 4096 for 12 bit) which is the max resolution of the analog pin
  
  // Approximated linear transfer function from datasheet
  // slightly less accurate but good at typical temps
   float vin = 3.3 * analogRead(DATA) / 4096.0;
 // Serial.print("LM19: ");
 // Serial.print("vin=");
//  Serial.print(vin);
 // Serial.print("  ");
  // plug in value to celcius temp equation
  float tempC = (1.8663 - vin) / 0.01169;
  // run celcius to fahrenheit conversion
  float tempF = 1.8 * tempC + 32.0;
  // print temperature to serial
 // Serial.print("tempC=");
 // Serial.print(tempC);
 // Serial.print("  ");
 // Serial.print("tempF=");
 // Serial.println(tempF);
 // Serial.println();

  printf("Temperature = %.1f C (%.1f F)\n", tempC, tempF);
  //delay(1000);
  
  // More accurate parabolic formula from the datasheet
  // Covers full temperature range of LM19
  
  vin = 3.3 * analogRead(0) / 4096.0;

/*
  Serial.print("LM19: ");
  Serial.print("vin=");
  Serial.print(vin);
  Serial.print("  ");

*/
  // Datasheet Formula: tempC = sqrt((2.1962 * 10^6) + ((1.8639 - vin)/(3.88 * 10^(-6)))) - 1481.96
   tempC = sqrt(2196200 + ((1.8639 - vin) / 0.00000388)) - 1481.96;
  tempF = 1.8 * tempC + 32.0;
  
  // print temperature to serial

/*
  Serial.print("tempC=");
  Serial.print(tempC);
  Serial.print("  ");
  Serial.print("tempF=");
  Serial.println(tempF);
  Serial.println();
*/

  delay(100);
  

 printf("Temperature part 2 = %.1f C (%.1f F)\n", tempC, tempF);
  
  // >>> End of LM19 Section <<<
}




int main(void)
{

	while(1)
	{
		
		loop();
		delay(1000);
	}


return(0);
}


