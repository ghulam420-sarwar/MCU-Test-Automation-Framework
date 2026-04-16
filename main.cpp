/**
 * Device Under Test (DUT) Firmware
 * --------------------------------
 * Simple command-response firmware used to exercise the MCU test-automation
 * framework. Accepts line-oriented ASCII commands over UART and responds with
 * OK/ERR + optional payload.
 *
 * Supported commands:
 *   PING             -> PONG
 *   ID?              -> OK <chip_id>
 *   ECHO <text>      -> OK <text>
 *   ADD <a> <b>      -> OK <sum>
 *   LED <0|1>        -> OK
 *   ADC?             -> OK <raw>
 *   VER?             -> OK 1.0.0
 *
 * Author: Ghulam Sarwar
 */

#include <Arduino.h>

constexpr uint8_t LED_PIN  = 2;
constexpr uint8_t ADC_PIN  = 34;
const char* FW_VERSION     = "1.0.0";

String buf;

void handle(const String& cmd) {
    if (cmd == "PING") {
        Serial.println("PONG");
    } else if (cmd == "ID?") {
        Serial.printf("OK %llX\n", ESP.getEfuseMac());
    } else if (cmd.startsWith("ECHO ")) {
        Serial.printf("OK %s\n", cmd.substring(5).c_str());
    } else if (cmd.startsWith("ADD ")) {
        int sp = cmd.indexOf(' ', 4);
        if (sp < 0) { Serial.println("ERR args"); return; }
        long a = cmd.substring(4, sp).toInt();
        long b = cmd.substring(sp + 1).toInt();
        Serial.printf("OK %ld\n", a + b);
    } else if (cmd.startsWith("LED ")) {
        digitalWrite(LED_PIN, cmd.substring(4).toInt() ? HIGH : LOW);
        Serial.println("OK");
    } else if (cmd == "ADC?") {
        Serial.printf("OK %u\n", analogRead(ADC_PIN));
    } else if (cmd == "VER?") {
        Serial.printf("OK %s\n", FW_VERSION);
    } else {
        Serial.println("ERR unknown");
    }
}

void setup() {
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(115200);
    delay(100);
    Serial.println("# DUT ready");
}

void loop() {
    while (Serial.available()) {
        char c = Serial.read();
        if (c == '\r') continue;
        if (c == '\n') {
            if (buf.length()) handle(buf);
            buf = "";
        } else if (buf.length() < 128) {
            buf += c;
        }
    }
}
