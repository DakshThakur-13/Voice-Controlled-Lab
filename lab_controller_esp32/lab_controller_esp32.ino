/*
 * ESP32 Lab Device Controller
 * 
 * Simple web server that controls lab equipment via GPIO pins.
 * Receives HTTP requests and toggles devices on/off.
 * 
 * Hardware connections:
 *   GPIO 25 - LED
 *   GPIO 33 - Projector relay
 *   GPIO 32 - Fan relay  
 *   GPIO 21 - Light relay
 */

#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi credentials - replace these or use secrets.h
#ifdef HAVE_SECRETS
#include "secrets.h"
#else
const char* ssid = "<YOUR_SSID>";
const char* password = "<YOUR_PASSWORD>";
#endif

WebServer server(80);

// Pin assignments
const int LED_PIN = 25;
const int PROJECTOR_PIN = 33;
const int FAN_PIN = 32;
const int LIGHT_PIN = 21;

// Simple helper to send HTTP 200 response
void respondOK(const char* msg) {
  server.send(200, "text/plain", msg);
}

// Device control handlers
void handleLedOn() { 
  digitalWrite(LED_PIN, HIGH); 
  respondOK("LED ON"); 
}

void handleLedOff() { 
  digitalWrite(LED_PIN, LOW); 
  respondOK("LED OFF"); 
}

void handleProjectorOn() { 
  digitalWrite(PROJECTOR_PIN, HIGH); 
  respondOK("Projector ON"); 
}

void handleProjectorOff() { 
  digitalWrite(PROJECTOR_PIN, LOW); 
  respondOK("Projector OFF"); 
}

void handleFanOn() { 
  digitalWrite(FAN_PIN, HIGH); 
  respondOK("Fan ON"); 
}

void handleFanOff() { 
  digitalWrite(FAN_PIN, LOW); 
  respondOK("Fan OFF"); 
}

void handleLightOn() { 
  digitalWrite(LIGHT_PIN, HIGH); 
  respondOK("Light ON"); 
}

void handleLightOff() { 
  digitalWrite(LIGHT_PIN, LOW); 
  respondOK("Light OFF"); 
}

// Health check endpoint
void handleStatus() {
  String response = "OK\n";
  response += "IP: ";
  response += WiFi.localIP().toString();
  respondOK(response.c_str());
}

void handleNotFound() {
  server.send(404, "text/plain", "Not Found");
}

void setup() {
  Serial.begin(115200);
  delay(200);

  // Configure GPIO pins as outputs
  pinMode(LED_PIN, OUTPUT);
  pinMode(PROJECTOR_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  // Start with all devices off
  digitalWrite(LED_PIN, LOW);
  digitalWrite(PROJECTOR_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(LIGHT_PIN, LOW);

  // Connect to Wi-Fi network
  Serial.printf("Connecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    
    // Give up after 15 seconds
    if (millis() - startTime > 15000) {
      Serial.println("\nConnection timeout");
      break;
    }
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Running without Wi-Fi");
  }

  // Register HTTP endpoints
  server.on("/led/on", handleLedOn);
  server.on("/led/off", handleLedOff);
  server.on("/projector/on", handleProjectorOn);
  server.on("/projector/off", handleProjectorOff);
  server.on("/fan/on", handleFanOn);
  server.on("/fan/off", handleFanOff);
  server.on("/light/on", handleLightOn);
  server.on("/light/off", handleLightOff);
  server.on("/status", handleStatus);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("Web server running");
}

void loop() {
  // Process incoming HTTP requests
  server.handleClient();
}