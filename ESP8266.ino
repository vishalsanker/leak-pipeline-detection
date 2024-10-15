#include <WiFi.h>
#include <ThingSpeak.h>

// Replace with your network credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// ThingSpeak channel details
unsigned long myChannelNumber = YOUR_CHANNEL_NUMBER;
const char* myWriteAPIKey = "YOUR_WRITE_API_KEY";

// WiFi client object
WiFiClient client;

float f1, f2, p;

void setup() {
  Serial.begin(9600);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected.");

  // Initialize ThingSpeak
  ThingSpeak.begin(client);
}

void loop() {
  if (Serial.available() > 0) {
    // Read incoming data from Arduino
    String data = Serial.readStringUntil('\n');
    // Assuming data format: "Flow Rate 1: XX.X L/H, Flow Rate 2: YY.Y L/H, Pressure: ZZ.Z"

    // Extract flow rates and pressure from the received data
    f1 = data.substring(data.indexOf(':') + 2, data.indexOf(" L/H")).toFloat();
    f2 = data.substring(data.indexOf(':', data.indexOf("L/H")) + 2, data.indexOf(" L/H", data.indexOf("L/H") + 1)).toFloat();
    p = data.substring(data.indexOf(':', data.indexOf(" L/H", data.indexOf("L/H") + 1)) + 2, data.indexOf(" K")).toFloat();

    // Print extracted values for debugging
    Serial.print("Flow Rate 1: ");
    Serial.println(f1);
    Serial.print("Flow Rate 2: ");
    Serial.println(f2);
    Serial.print("Pressure: ");
    Serial.println(p);

    // Write data to ThingSpeak fields
    ThingSpeak.setField(1, f1);
    ThingSpeak.setField(2, f2);
    ThingSpeak.setField(3, p);

    // Write the data to ThingSpeak
    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    if (x == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }

    // Delay for data to be sent (adjust as needed)
    delay(20000); // ThingSpeak only allows updates every 15 seconds
  }
}
