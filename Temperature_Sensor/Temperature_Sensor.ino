//Yellow Wire - A0
//Black Wire - GND
//Red Wire - 3.3V

const int temperaturePin = A0;

void setup()
{
  Serial.begin(9600);
}


void loop()
{
  float voltage, degreesC, degreesF;
  Serial.println(analogRead(temperaturePin));
  voltage = analogRead(temperaturePin) * 0.004882814;
  
  degreesC = (voltage - 0.5) * 100.0;

  degreesF = degreesC * (9.0/5.0) + 32.0;

  // Now we'll use the serial port to print these values
  
  Serial.print("voltage: ");
  Serial.print(voltage);
  Serial.print("  deg C: ");
  Serial.print(degreesC);
  Serial.print("  deg F: ");
  Serial.println(degreesF);

  delay(1000); // repeat once per second (change as you wish!)
}

