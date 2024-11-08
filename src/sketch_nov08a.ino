#include <WiFi.h>

// List of authorized networks
const char* authorized_networks[] = {"Home_Network", "Office_WiFi"};
const int num_authorized_networks = sizeof(authorized_networks) / sizeof(authorized_networks[0]);

// Function to check if a network is authorized
bool isAuthorizedNetwork(const char* ssid) {
  for (int i = 0; i < num_authorized_networks; i++) {
    if (strcmp(ssid, authorized_networks[i]) == 0) {
      return true;
    }
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("ESP32 Wi-Fi Network Scanner and Unauthorized Network Detector");
}

void loop() {
  Serial.println("Scanning for Wi-Fi networks...");
  int num_networks = WiFi.scanNetworks();

  if (num_networks == 0) {
    Serial.println("No Wi-Fi networks found.");
  } else {
    for (int i = 0; i < num_networks; i++) {
      String ssid = WiFi.SSID(i);
      int rssi = WiFi.RSSI(i);

      Serial.print("Network found: ");
      Serial.print(ssid);
      Serial.print(" (RSSI: ");
      Serial.print(rssi);
      Serial.println(")");

      // Check if the network is unauthorized
      if (!isAuthorizedNetwork(ssid.c_str())) {
        Serial.print("⚠️ ALERT: Unauthorized Network Detected - ");
        Serial.println(ssid);
      }
    }
  }

  // Wait 10 seconds before scanning again
  delay(10000);
}
