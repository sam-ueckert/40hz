/**
 * 40Hz Gamma Stimulation Controller
 * 
 * Drives an LED via MOSFET at precisely 40Hz using hardware timer.
 * Target: Seeed XIAO ESP32-C3
 * 
 * Wiring:
 *   GPIO2 -> IRLZ44N Gate (with 10K pulldown to GND)
 *   IRLZ44N Drain <- LED (-)
 *   IRLZ44N Source -> GND
 *   LED (+) <- 12V+
 */

#include <Arduino.h>

// === Configuration ===
#define LED_PIN           2       // GPIO pin driving MOSFET gate
#define FREQUENCY_HZ      40      // Target frequency
#define DUTY_CYCLE        0.5     // 50% duty cycle (equal on/off)
#define SESSION_MINUTES   60      // Auto-stop after this many minutes (0 = continuous)
#define SERIAL_BAUD       115200

// === Derived constants ===
const uint32_t periodUs    = 1000000UL / FREQUENCY_HZ;              // 25000us for 40Hz
const uint32_t onTimeUs    = (uint32_t)(periodUs * DUTY_CYCLE);     // 12500us
const uint32_t offTimeUs   = periodUs - onTimeUs;                    // 12500us
const uint32_t sessionUs   = (uint32_t)SESSION_MINUTES * 60UL * 1000000UL;

// === State ===
hw_timer_t *timer = NULL;
volatile bool ledState = false;
volatile uint32_t cycleCount = 0;
uint32_t startTimeUs = 0;
bool running = true;

void IRAM_ATTR onTimer() {
  ledState = !ledState;
  digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  if (ledState) cycleCount++;
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(1000);
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("========================================");
  Serial.println("  40Hz Gamma Stimulation Controller");
  Serial.println("========================================");
  Serial.printf("  Frequency:    %d Hz\n", FREQUENCY_HZ);
  Serial.printf("  Period:       %lu us\n", periodUs);
  Serial.printf("  On time:      %lu us\n", onTimeUs);
  Serial.printf("  Off time:     %lu us\n", offTimeUs);
  Serial.printf("  Duty cycle:   %.0f%%\n", DUTY_CYCLE * 100);
  Serial.printf("  Session:      %d min%s\n", SESSION_MINUTES, 
                SESSION_MINUTES == 0 ? " (continuous)" : "");
  Serial.printf("  GPIO pin:     %d\n", LED_PIN);
  Serial.println("========================================");
  Serial.println("  Starting stimulation...");
  Serial.println();
  
  startTimeUs = micros();
  
  // Hardware timer: fire every half-period (toggle on/off)
  // Timer 0, prescaler 80 (1MHz tick), count up
  timer = timerBegin(1000000);  // 1MHz
  timerAttachInterrupt(timer, &onTimer);
  timerAlarm(timer, onTimeUs, true, 0);  // auto-reload
}

void loop() {
  static uint32_t lastReport = 0;
  uint32_t now = millis();
  
  // Report every 10 seconds
  if (now - lastReport >= 10000) {
    lastReport = now;
    uint32_t elapsed = (now - startTimeUs / 1000) / 1000;
    uint32_t minutes = elapsed / 60;
    uint32_t seconds = elapsed % 60;
    Serial.printf("[%02lu:%02lu] Cycles: %lu  (%.1f Hz actual)\n",
                  minutes, seconds, cycleCount,
                  cycleCount > 0 ? (float)cycleCount / ((float)elapsed) : 0.0);
  }
  
  // Session timeout
  if (SESSION_MINUTES > 0 && running) {
    uint32_t elapsedMs = now - (startTimeUs / 1000);
    if (elapsedMs >= (uint32_t)SESSION_MINUTES * 60UL * 1000UL) {
      timerDetachInterrupt(timer);
      digitalWrite(LED_PIN, LOW);
      running = false;
      Serial.println();
      Serial.println("========================================");
      Serial.printf("  Session complete: %d minutes\n", SESSION_MINUTES);
      Serial.printf("  Total cycles: %lu\n", cycleCount);
      Serial.println("========================================");
    }
  }
  
  delay(100);
}
