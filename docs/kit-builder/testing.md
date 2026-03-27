# Component Testing

Use these procedures to verify each component works before kit assembly.

## LED Brick

1. Set a variable power supply to 3.3V.
2. Connect the supply positive to the red wire and ground to the black wire.
3. The LED should draw approximately 0.02–0.03A and light up brightly.

## Sensor Brick

1. Apply +3.3V from a power supply to the white wire (+3.3V) and connect the supply ground to
   the blue wire (GND).
2. Use a multimeter with one lead on the supply ground and the other on the yellow signal wire.
3. Measure voltage in light and in darkness — the signal voltage should be **high in light and
   low in dark**.

> **Note:** If the reading is reversed, swap the +3.3V and GND wires.
> A resting voltage of around 2–2.3V in typical indoor lighting is normal.

## Neopixel Brick

1. Using a test Pico running the standard firmware, connect the Neopixel's +5V, GND, and DIN
   pins to the corresponding Pico pins (see the [Wiring Guide](wiring-guide.md)).
2. Power the Pico via USB.
3. Confirm the rainbow animation plays on startup.

## Fan

1. Set a power supply to 5V.
2. Connect the fan wires to +5V and GND.
3. The fan should spin and blow air.

## Pico Board — Pre-Completion

1. After soldering the Neopixel brick to the Pico, power it via USB.
2. Confirm the Neopixel strip runs the startup sequence correctly before continuing assembly.

## Pico Board — Post-Completion

1. Construct a demo LEGO enclosure that allows easy swapping of sensor components.
2. For each assembled wire harness, connect the sensor brick, fan, and LED brick in turn.
3. Verify the complete startup and calibration sequence runs and the sensor responds to changes
   in light.

## Mist Generator

1. After full assembly, plug the mist generator into the wall.
2. Squeeze the red pump — the generator should produce mist.
