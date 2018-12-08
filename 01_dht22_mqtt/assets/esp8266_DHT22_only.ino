/** 
 *  Required libraries:
 *    - DHT sensor library by Adafruit
 *    - Adafruit Unified Sensor
**/

#include <DHT.h>

#define DHTPIN D4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

float humidity;
float temperature;

void setup() {
  Serial.begin(115200);
  while (! Serial);

  dht.begin();
}

void loop() {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("DHT22 sensor is not ready yet");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" | Humidity: ");
  Serial.println(humidity);

  delay(5000);
}
