
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// By: Alex Szebrag
// NOTE: YOU WILL ALSO REQUIRED THE FOLLOWING FILE: NewliquidCrystal_1.3.4.zip for this code to work!

LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3,POSITIVE); //ensure LCD is set properly
int tempsensingPin = 0; // pin A0 for digital temperature value (input)
int lightsensingPin = 1 ; // pin A1 for digital lighting value (input)
int digital_temp_val = 0; // variable to store the read temp value (digital) from temp sensor
int digital_lighting_val = 0; // variable to store the read light intensity value (digital) from photodiode
int fanpin1 = 13; //pin D13 - relay for cooling fan (output)
int fanpin2 = 12; //pin D12 - relay for heating fan (output)
int LEDpin1 = 41; //pin D41 - LED1 (output)
int LEDpin2 = 42; //pin D42 - LED2 (output)
int LEDpin3 = 11; //pin D11 - LED3 (output)
int LEDpin4 = 10; //pin D10 - LED4 (output)
int LEDpin5 = 9;  //pin D9  - LED5 (output)
int LEDpin6 = 8;  //pin D8  - LED6 (output)
int LEDpin7 = 7;  //pin D7  - LED7 (output)
double temperature = 0.0; //init temperature in degrees C
double analog_voltage_light_sensor = 0.0; //init analog voltage of light sensor (from the 1k resistor)
double LUX = 0.0; //init illuminance (calculated based on the fact that we know 1uA = 1LUX... 1mV = 1LUX)  

//setup input/output pins and character LCD
void setup()
{
  Serial.begin(9600); // setup serial communication
  pinMode(fanpin1, OUTPUT); //put digital pin 13 as output (to relay for cooling FAN)
  pinMode(fanpin2, OUTPUT); //put digital pin 12 as output (to relay for heating FAN)
  pinMode(LEDpin1, OUTPUT); //put digital pin 41 as output (to LED1)
  pinMode(LEDpin2, OUTPUT); //put digital pin 42 as output (to LED2)
  pinMode(LEDpin3, OUTPUT); //put digital pin 11 as output (to LED3)
  pinMode(LEDpin4, OUTPUT); //put digital pin 10 as output (to LED4)
  pinMode(LEDpin5, OUTPUT); //put digital pin 9 as output (to LED5)
  pinMode(LEDpin6, OUTPUT); //put digital pin 8 as output (to LED6)
  pinMode(LEDpin7, OUTPUT); //put digital pin 7 as output (to LED7)
  pinMode(tempsensingPin, INPUT); //put analog pin 0 as input (from temperature sensor)
  pinMode(lightsensingPin, INPUT); //put analog pin 1 as input (from light sensor)
  lcd.begin(16,2); //start the LCD
  lcd.backlight(); //turn on LCD screen backlight
 
}

//data processing, logic control, LCD output
void loop()
{
  digital_temp_val = analogRead(tempsensingPin); // read the input pin, ADC on temp sensor value done here
  digital_lighting_val = analogRead(lightsensingPin); // read the input pin, ADC on light sensor value done here
  
  temperature = (digital_temp_val - 270.072)/(4.092); //temperature = (digital code - digital code offset at 0 degrees C )/ (digital code/1 degree celcius)
  analog_voltage_light_sensor = (0.004887585) * (digital_lighting_val); //analog voltage and digital code relationship -> V = (5/1023) * digital code
  LUX = 4.88758553*digital_lighting_val ; //LUX digital code relationship

  //for debugging (commented out):
  /*
  Serial.println("The temperature sensor values are: ");
  Serial.println(digital_temp_val);             // debug temperature digital value
  Serial.println(temperature); //debug actual temperature in degrees C
  Serial.println("The light sensor values are: ");
  Serial.println(digital_lighting_val);
  Serial.println(analog_voltage_light_sensor); // debug analog voltage of light sensor
  Serial.println(LUX); //debug LUX value of sensor
  */
  
  delay (1000); //add a delay (1s) between each subsequent LCD outputs 
  lcd.clear();
  lcd.print("Temp:         C  ");
  lcd.setCursor(6, 0);
  lcd.print(temperature); //print temp in degrees C on character LCD (1st line)

  //other temperature values (digital = temp): 344 = 18, 348 = 19, 352 = 20, 357 = 21, 361 = 22, 369 = 24, 377 = 26, 381 = 27  , 372 = old = 24.91, 365 = 23

  
  //temperature logic control:
  
  if(digital_temp_val >= 372) //temp >= 25 degrees C 
  {
      digitalWrite(fanpin1,HIGH); //turn cooling fan on
      digitalWrite(fanpin2,LOW); //turn heating fan off
  }

  if (digital_temp_val <= 365) // temp <= 23 degrees C 
  {
    digitalWrite(fanpin1,LOW); //turn cooling fan off
    digitalWrite(fanpin2,HIGH); //turn heating fan on
  }


  //LED/lighting control/logic:

  //init all LEDs to off
  digitalWrite(LEDpin7,LOW);
  digitalWrite(LEDpin6,LOW); 
  digitalWrite(LEDpin5,LOW);
  digitalWrite(LEDpin4,LOW); 
  digitalWrite(LEDpin3,LOW);
  digitalWrite(LEDpin2,LOW);
  digitalWrite(LEDpin1,LOW); 

  //light intensity = LUX = digital code relationship: 
  // 0 = LUX<10 = 0<= digital code < 3 (7 LEDs on)
  // 1 = 10<=LUX<20 = 3<= digital code < 5 (6 LEDs on)
  // 2 = 20<=LUX<50 = 5<= digital code < 11 (5 LEDs on)
  // 3 = 50<=LUX<100 = 11<= digital code < 21 (4 LEDs on)
  // 4 = 100<=LUX<150 = 21<= digital code < 31 (3 LEDs on)
  // 5 = 150<=LUX<250 = 31<= digital code < 52 (2 LEDs on)
  // 6 = 250<=LUX<500 = 52<= digital code < 103 (1 LED on)
  // 7 = 500<=LUX<750 = 103<= digital code < 154 (0 LEDs on) TARGET LEVEL
  // 8 = 750<=LUX<1000 = 154<= digital code < 205 (0 LEDs on)
  // 9 = 1000<=LUX<1500 = 205<= digital code < 307 (0 LEDs on)
  // 10 = 1500<=LUX<2000 = 307<= digital code < 410 (0 LEDs on)
  // 11 = 2000<=LUX<5000 = 410<= digital code < 1023 (0 LEDs on)
  // 7 = 5000 LUX = digital code 1023 (0 LEDs on)


  //case in which at least 1 LED needs to be turned on (intensity <=6)
  if(digital_lighting_val<103)
  {
    //intensity = 6
    if(digital_lighting_val>=52)
    {
      digitalWrite(LEDpin1,HIGH); 
    }

    //intesnity = 5
    if(digital_lighting_val >=31 && digital_lighting_val < 52)
    {
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH); 
    }

    //intensity > 5
    else
    {
      digitalWrite(LEDpin2,LOW);
    }
    
    //intensity = 4
    if(digital_lighting_val >=21 && digital_lighting_val < 31)
    {
      digitalWrite(LEDpin3,HIGH);
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH);  
    }

    //intensity > 4
    else
    {
      digitalWrite(LEDpin3,LOW);
    }

    //intensity = 3
    if(digital_lighting_val >= 11 && digital_lighting_val < 21)
    {
      digitalWrite(LEDpin4,HIGH);
      digitalWrite(LEDpin3,HIGH);
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH); 
    }

    //intensity > 3
    else
    {
      digitalWrite(LEDpin4,LOW);
    }

    //intensity = 2
    if(digital_lighting_val >= 5 && digital_lighting_val < 11)
    {
      digitalWrite(LEDpin5,HIGH);
      digitalWrite(LEDpin4,HIGH); 
      digitalWrite(LEDpin3,HIGH);
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH);  
    }

    //intensity >2
    else
    {
      digitalWrite(LEDpin5,LOW);
    }

    //intensity = 1
    if(digital_lighting_val >= 3 && digital_lighting_val < 5)
    {
      digitalWrite(LEDpin6,HIGH);
      digitalWrite(LEDpin5,HIGH);
      digitalWrite(LEDpin4,HIGH); 
      digitalWrite(LEDpin3,HIGH);
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH);  
    }

    //intensity >1
    else
    {
      digitalWrite(LEDpin6,LOW);
    }

    //intensity = 0
    if(digital_lighting_val >= 0 && digital_lighting_val < 3)
    {
      digitalWrite(LEDpin7,HIGH);
      digitalWrite(LEDpin6,HIGH); 
      digitalWrite(LEDpin5,HIGH);
      digitalWrite(LEDpin4,HIGH); 
      digitalWrite(LEDpin3,HIGH);
      digitalWrite(LEDpin2,HIGH);
      digitalWrite(LEDpin1,HIGH); 
    }

    //intensity > 0
    else
    {
      digitalWrite(LEDpin7,LOW);
    }

  }

  //case in which intesnity level >=7 (no LEDs turn on)
  else
  {
    digitalWrite(LEDpin1,LOW);       
  }


  //display on LCD Light stats (LUX and intensity (I))

  lcd.setCursor(0, 1); //set to 2nd col of LCD for light value stats
  lcd.print("LUX=");
  lcd.print(LUX);
  lcd.print(",I="); //intensity level (between 0 - 11)
        
  if(digital_lighting_val < 3 && digital_lighting_val >= 0)
    lcd.print("0"); //intensity level 0 (darkest - all lights on)
  if(digital_lighting_val < 5 && digital_lighting_val >=3)
    lcd.print("1");
  if(digital_lighting_val < 11 && digital_lighting_val >= 5)
    lcd.print("2"); 
  if(digital_lighting_val < 21 && digital_lighting_val >=11)
    lcd.print("3");
  if(digital_lighting_val < 31 && digital_lighting_val >=21)
    lcd.print("4");
  if(digital_lighting_val < 52 && digital_lighting_val >= 31)
    lcd.print("5"); 
  if(digital_lighting_val < 103 && digital_lighting_val >=52)
    lcd.print("6");
  if(digital_lighting_val < 154 && digital_lighting_val >=103)
    lcd.print("7");
  if(digital_lighting_val < 205 && digital_lighting_val >= 154)
    lcd.print("8"); 
  if(digital_lighting_val < 307 && digital_lighting_val >=205)
    lcd.print("9");
  if(digital_lighting_val < 410 && digital_lighting_val >=307)
    lcd.print("10");
  if(digital_lighting_val < 1023 && digital_lighting_val >= 410)
    lcd.print("11"); 
  if(digital_lighting_val == 1023)
    lcd.print("12");     
}

