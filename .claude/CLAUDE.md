## Project Overview

LEGO Air Quality Monitor — an educational STEM kit by Case Western Reserve University (ISSACS).
A Raspberry Pi Pico reads an analog light/pollution sensor and displays levels on an 8-LED
WS2812B Neopixel bar, housed in 3D-printed LEGO-compatible bricks.

## Repository Structure

- **Software/** — MicroPython firmware for Raspberry Pi Pico (RP2040)
  - `main.py` is the canonical source; the Pico automatically runs `main.py` on boot
  - `legobrickscript.py` is a legacy duplicate — pending removal
- **Models/** — 3D CAD (STL/STEP/SLDPRT) and Eagle CAD PCB design files (EPAPollutionMonV101)
- **Technical Documentation/** — Build docs, BOM, wiring guide, troubleshooting (docx/xlsx)
- **Instructor Documentation/** — Student-facing assembly tutorials and technical explanations

## Firmware Architecture (Software/main.py)

Single-file MicroPython program with these key sections:

1. **WS2812B PIO driver** (lines ~45-64) — Custom RP2040 PIO assembly for Neopixel bit-banging at 8MHz
2. **LED helpers** — `pixels_show()`, `pixels_fill()`, `pixels_fill_partial()`, `color_chase()`, `rainbow_cycle()`
3. **Sensor init** (`init_sensor_unit()`) — Validates sensor by toggling white LED and checking ADC differential
4. **Baseline calibration** (`read_baseline()`) — 3-second window capturing min/max/mean sensor range
5. **Main loop** — Two-stage signal filtering (exponential smoothing τ=200ms + 20-sample rolling average), maps filtered value to 0-8 LED bar

**Hardware pins:** GPIO 15 (white status LED), GPIO 22 (Neopixel data), ADC 26 (sensor input)

## Deploying to Pico

1. Hold BOOTSEL, plug in Pico, drag a MicroPython UF2 firmware file to the USB drive
   - `Software/rp2-pico-20210618-v1.16.uf2` is included but is from 2021 — pending decision on whether to replace with a link to the official MicroPython download
2. Open Thonny, select COM port, save `Software/main.py` to Pico as `main.py`
3. Ctrl+D to reboot — firmware auto-runs

## License

MIT License — Copyright (c) 2021 Case Western Reserve University Institute for Smart, Secure and Connected Systems.
Hardware design files and educational content may move to CC BY 4.0 in the future.

## Current Status

This repo is being prepared for public release. In progress:
- Documentation is being migrated from `.docx`/`.xlsx` to Markdown
- `legobrickscript.py` is pending removal in favor of `main.py`
- UF2 firmware inclusion is under review
- Hardware files (`Models/EPAPollutionMonV101/`) are not yet committed

## Key Constraints

- MicroPython v1.16 on RP2040 — no pip packages, standard library only
- No build system, linter, or test framework in the repo
- All timing-critical LED control uses PIO state machines, not CPU bit-banging
- Brightness capped at 20% (`brightness = 0.2`) to conserve power
