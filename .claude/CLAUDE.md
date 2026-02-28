## Project Overview

LEGO Air Quality Monitor — an educational STEM kit by Case Western Reserve University (ISSACS).
Participants build a physical model of an optical air quality sensor: a LEGO brick structure
channels water vapor between a white LED and a photoreceptor, simulating how particulate matter
scatters light in a real PM sensor. Readings are displayed on an 8-LED WS2812B Neopixel bar.

## Repository Structure

- **firmware/** — MicroPython firmware for Raspberry Pi Pico (RP2040)
  - `main.py` is the canonical source; the Pico automatically runs `main.py` on boot
- **Models/** — 3D CAD (STL/STEP/SLDPRT) and Eagle CAD PCB design files (EPAPollutionMonV101)
- **docs/** — Audience-organized documentation (kit-builder, instructor, participant)
  - `docs/kit-builder.md` contains the original README assembly/setup content (image paths need fixing)
  - `Technical Documentation/` and `Instructor Documentation/` are legacy — being migrated to `docs/`

## Firmware Architecture (firmware/main.py)

Single-file MicroPython program with these key sections:

1. **WS2812B PIO driver** (lines ~45-64) — Custom RP2040 PIO assembly for Neopixel bit-banging at 8MHz
2. **LED helpers** — `pixels_show()`, `pixels_fill()`, `pixels_fill_partial()`, `color_chase()`, `rainbow_cycle()`
3. **Sensor init** (`init_sensor_unit()`) — Validates sensor by toggling white LED and checking ADC differential
4. **Baseline calibration** (`read_baseline()`) — 3-second window capturing min/max/mean sensor range
5. **Main loop** — Two-stage signal filtering (exponential smoothing τ=200ms + 20-sample rolling average), maps filtered value to 0-8 LED bar

**Hardware pins:** GPIO 15 (white status LED), GPIO 22 (Neopixel data), ADC 26 (sensor input)

## Deploying to Pico

1. Hold BOOTSEL, plug in Pico, drag the MicroPython UF2 to the USB drive
   - Download from https://micropython.org/download/RPI_PICO/
2. Open Thonny, select COM port, save `firmware/main.py` to Pico as `main.py`
3. Ctrl+D to reboot — firmware auto-runs

## License

MIT License — Copyright (c) 2021 Case Western Reserve University Institute for Smart, Secure and Connected Systems.
Hardware design files and educational content may move to CC BY 4.0 in the future.

## Current Status

This repo is being prepared for public release. In progress:
- Documentation is being migrated from `.docx`/`.xlsx` to Markdown under `docs/`
- Hardware files (`Models/EPAPollutionMonV101/`) are not yet committed

## Key Constraints

- MicroPython v1.16 on RP2040 — no pip packages, standard library only
- No build system, linter, or test framework in the repo
- All timing-critical LED control uses PIO state machines, not CPU bit-banging
- Brightness capped at 20% (`brightness = 0.2`) to conserve power
