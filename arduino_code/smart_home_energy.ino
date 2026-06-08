#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* TS_SERVER = "http://thingspeak.com";
String TS_API_KEY = "MZDPB53412RWH90L"; 

const int CURRENT_PIN = 34; 
const float VOLTAGE_NOMINAL = 230.0; 
const float CALIBRATION_FACTOR = 0.058; 

double total_watt_hours = 0.0;
unsigned long time_marker_previous = 0;

void setup() {
    Serial.begin(115200);
    pinMode(CURRENT_PIN, INPUT);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
    time_marker_previous = millis();
}

void loop() {
    long accumulation_sum = 0;
    int samples = 0;
    unsigned long duration_start = millis();

    while (millis() - duration_start < 200) {
        int sample_raw = analogRead(CURRENT_PIN);
        long sample_offset = sample_raw - 2048; 
        accumulation_sum += (sample_offset * sample_offset);
        samples++;
    }

    float rms_current = sqrt((float)accumulation_sum / samples) * CALIBRATION_FACTOR;
    if (rms_current < 0.08) rms_current = 0.0; 

    float active_power = VOLTAGE_NOMINAL * rms_current;
    unsigned long time_marker_current = millis();
    double tracking_interval = (time_marker_current - time_marker_previous) / 3600000.0; 
    time_marker_previous = time_marker_current;

    total_watt_hours += active_power * tracking_interval;
    float cost = (total_watt_hours / 1000.0) * 6.50;
    float alert = (rms_current > 15.0) ? 1.0 : 0.0;

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = String(TS_SERVER) + "/update?api_key=" + TS_API_KEY +
                     "&field1=" + String(VOLTAGE_NOMINAL) + "&field2=" + String(rms_current) +
                     "&field3=" + String(active_power) + "&field4=" + String(total_watt_hours) +
                     "&field5=" + String(cost) + "&field6=" + String(alert);
        http.begin(url);
        http.GET();
        http.end();
    }
    delay(15000); 
}