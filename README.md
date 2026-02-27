# 40Hz Gamma Stimulation Device

A simple, low-cost device that strobes an LED light at 40Hz for gamma-frequency visual stimulation.

## Background

A growing body of research suggests that 40Hz sensory stimulation (light and/or sound) may help clear amyloid-beta plaques associated with Alzheimer's disease by activating the brain's glymphatic waste-clearance system.

### Key Studies

- **Iaccarino et al. (2016) — Nature**: MIT showed 40Hz flickering light reduced amyloid-beta levels in Alzheimer's transgenic mice. [DOI: 10.1038/nature20587](https://doi.org/10.1038/nature20587)
- **Martorell et al. (2019) — Cell**: Combined 40Hz light + sound reduced amyloid and tau across broader brain regions. [DOI: 10.1016/j.cell.2019.02.014](https://doi.org/10.1016/j.cell.2019.02.014)
- **Wang et al. (2026) — PNAS**: First primate evidence. 9 aged rhesus macaques showed ~200% increase in CSF amyloid-beta clearance after 1 week of 40Hz auditory stimulation, with effects lasting 5+ weeks. [DOI: 10.1073/pnas.2529565123](https://doi.org/10.1073/pnas.2529565123)
- **Cognito Therapeutics OVERTURE (2024)**: Human trial showed 76% reduction in cognitive decline, 77% reduction in functional decline, 69% reduction in brain atrophy over 6 months. [DOI: 10.3389/fneur.2024.1343588](https://doi.org/10.3389/fneur.2024.1343588)
- **Chan et al. (2025)**: 2-year open-label extension in mild AD patients showed decreased plasma pTau217 by up to 47%. [DOI: 10.1002/alz.70792](https://doi.org/10.1002/alz.70792)

### Mechanism

The 40Hz stimulation entrains gamma oscillations in the brain. Interneurons release VIP peptide, which activates the glymphatic system to flush amyloid-beta from brain tissue into cerebrospinal fluid. The stimulation also increases microglia and astrocyte activity, improving clearance of amyloid plaques.

## Hardware

### Parts List

| Part | Specific Item | Approx. Cost |
|------|--------------|-------------|
| Microcontroller | [Seeed XIAO ESP32-C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) (USB-C, WiFi, BLE) | ~$5 |
| MOSFET | IRLZ44N logic-level N-channel | ~$1.50 |
| Gate resistor | 10KΩ pulldown | ~$0.10 |
| LED light | 12V LED corn bulb, E26 base, 10-15W (~100W equiv.) | ~$6 |
| Socket | E26 lamp socket with leads | ~$4 |
| Power supply | 12V 2A DC adapter | ~$8 |
| Breadboard + wires | Starter pack with jumper wires | ~$5 |
| **Total** | | **~$30** |

### Why DC LED, Not AC Household Bulb?

AC LED household bulbs have internal rectifiers and smoothing capacitors that keep the LED lit for milliseconds after power is cut — this destroys 40Hz precision. DC LEDs respond instantly to on/off signals, producing a clean square wave.

### Wiring Diagram

```
ESP32-C3 GPIO2 ──┬── IRLZ44N Gate
                 │
               10KΩ
                 │
                GND

12V+ ──── LED Bulb (+) ──── LED Bulb (-) ──── IRLZ44N Drain

IRLZ44N Source ──── GND

12V PSU GND ──── ESP32 GND (common ground)
```

### Pin Assignment

| ESP32-C3 Pin | Function |
|-------------|----------|
| GPIO2 | MOSFET gate (LED strobe control) |
| 5V | Powered via USB-C |
| GND | Common ground with 12V supply |

## Firmware

See [`src/main.cpp`](src/main.cpp) for the Arduino firmware.

### Features

- Precise 40Hz square wave output (25ms period: 12.5ms on, 12.5ms off)
- Hardware timer-based for accuracy (not software delay)
- Serial output for monitoring
- Configurable frequency and duty cycle

### Building

1. Install [PlatformIO](https://platformio.org/) or Arduino IDE
2. Select board: **Seeed XIAO ESP32-C3**
3. Upload `src/main.cpp`
4. Open serial monitor at 115200 baud to confirm 40Hz output

## Future Additions

- [ ] 40Hz audio tone output (1kHz carrier pulsed at 40Hz, per Wang et al. 2026 protocol)
- [ ] Combined audiovisual mode
- [ ] WiFi control interface for frequency/duty cycle adjustment
- [ ] Session timer (1-hour sessions per research protocols)
- [ ] Session logging
- [ ] BLE companion app

## Safety

⚠️ **This is not a medical device.** This is a research/hobby project inspired by published studies. 40Hz flickering light may trigger seizures in people with photosensitive epilepsy. Consult a physician before use, especially if you have any history of seizures or epilepsy.

## License

MIT
