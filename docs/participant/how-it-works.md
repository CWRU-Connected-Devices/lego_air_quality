# How It Works

## Startup and Calibration

When the microcontroller powers on, it runs through a calibration sequence to verify the
sensor assembly and establish a baseline reading. The LED bar signals each phase:

### Rainbow Phase

The microcontroller begins with a quick rainbow animation to confirm it has powered on
successfully.

### Yellow Phase

The microcontroller reads the light sensor before and after turning the white LED on. If both
readings are the same, it means the sensor cannot detect the LED — likely an assembly issue.
The lights will turn purple to signal the error.

### Cyan Phase

If the yellow phase passes, the microcontroller turns the white LED on and records a series of
sensor readings over two seconds. It remembers the largest and smallest values, which are used
as the baseline range in the next phase.

### Red Phase

The sensor is now actively measuring. Each reading goes through this loop:

1. Read the light sensor
2. Update the remembered minimum and maximum values if a new extreme is detected
3. Divide the range between minimum and maximum into 8 equal sections — one per LED
4. Light up the number of red LEDs corresponding to which section the current reading falls in
5. Repeat

## Why Early Readings Seem Off

Right after calibration, the air quality will likely read higher than expected — even in clean
air. At that point, the microcontroller has only seen a narrow range of values, so the 8
sections are very small and tiny fluctuations move the reading significantly.

Once you introduce particulate matter — in this kit, mist from the mist generator simulates
airborne particles — a new maximum is recorded and the range expands. The sensor becomes more
accurate and responsive as it sees a wider range of values.

## Components

### Raspberry Pi Pico

The "brain" of the sensor is a Raspberry Pi Pico — a small programmable computer that runs
Python. It has 40 pins that can be used to control and read sensors, lights, and other
components.

### LED Brick

The LED brick houses a white LED that illuminates when powered by the Pico. The brick was
custom-designed in CAD software, 3D-printed, and can be printed in any color.

### Sensor Brick

The sensor brick contains a photoresistor — an electrical component that changes its resistance
based on how much light hits it. More light means less resistance; less light means more
resistance. Like the LED brick, it was custom-designed, 3D-printed, and can be any color.

### Display

The display brick holds a strip of 8 Neopixels. Each Neopixel is an RGB LED containing
individual red, green, and blue elements — and each can be controlled independently in color
and brightness, all from just three wires.
