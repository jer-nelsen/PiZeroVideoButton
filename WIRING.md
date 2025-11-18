# GPIO Wiring Guide for Pi Zero Video Button

## Raspberry Pi Zero W 2 Pinout Reference

```
                    3.3V  [ 1] [ 2]  5V
                GPIO 2  [ 3] [ 4]  5V
                GPIO 3  [ 5] [ 6]  GND
                GPIO 4  [ 7] [ 8]  GPIO 14
                   GND  [ 9] [10]  GPIO 15
  -->  BUTTON   GPIO 17 [11] [12]  GPIO 18
               GPIO 27  [13] [14]  GND
               GPIO 22  [15] [16]  GPIO 23
                  3.3V  [17] [18]  GPIO 24
               GPIO 10  [19] [20]  GND
                GPIO 9  [21] [22]  GPIO 25
               GPIO 11  [23] [24]  GPIO 8
                   GND  [25] [26]  GPIO 7
                GPIO 0  [27] [28]  GPIO 1
                GPIO 5  [29] [30]  GND
                GPIO 6  [31] [32]  GPIO 12
               GPIO 13  [33] [34]  GND
               GPIO 19  [35] [36]  GPIO 16
               GPIO 26  [37] [38]  GPIO 20
                   GND  [39] [40]  GPIO 21
```

## Component Wiring

### Momentary Push Button

**Connection Type:** Normally Open (NO) momentary button

```
Raspberry Pi Zero              Momentary Button
┌─────────────────┐           ┌──────────────┐
│                 │           │              │
│  Pin 11 (GPIO17)├───────────┤ Signal       │
│                 │           │              │
│  Pin 9 (GND)    ├───────────┤ Ground       │
│                 │           │              │
└─────────────────┘           └──────────────┘
```

**Configuration:**
- GPIO 17 is configured with internal pull-up resistor (3.3V when not pressed)
- Button press connects GPIO 17 to Ground (0V)
- This creates a FALLING edge trigger
- No external resistors needed for button signal

### LED (Integrated or Separate)

#### Option 1: LED Integrated with Button (Common)

If your button has an integrated LED that requires 5V:

```
Raspberry Pi Zero              Button with LED
┌─────────────────┐           ┌──────────────┐
│                 │           │              │
│  Pin 2 (5V)     ├───────────┤ LED+ (5V)    │
│                 │           │              │
│  Pin 6 (GND)    ├───────────┤ LED- (GND)   │
│                 │           │              │
│  Pin 11 (GPIO17)├───────────┤ Button Signal│
│                 │           │              │
│  Pin 9 (GND)    ├───────────┤ Button GND   │
│                 │           │              │
└─────────────────┘           └──────────────┘
```

#### Option 2: Separate LED

If you have a separate LED:

```
Raspberry Pi Zero                       LED
┌─────────────────┐
│                 │
│  Pin 2 (5V)     ├────[Resistor]────[+LED-]────┐
│                 │      220-330Ω                │
│  Pin 6 (GND)    ├──────────────────────────────┘
│                 │
└─────────────────┘
```

**Important LED Notes:**
- Always use a current-limiting resistor with LEDs
- For 5V supply: Use 220-330Ω resistor
- For 3.3V supply: Use 100-150Ω resistor
- LED polarity matters: Long leg = Positive (+), Short leg = Negative (-)

## Complete Wiring Diagram

### Typical Setup with Integrated LED Button

```
┌───────────────────────────────────────────┐
│        Raspberry Pi Zero W 2              │
│                                           │
│  [1] 3.3V                          5V [2] ├──────┐
│  [3] GPIO2                         5V [4] │      │
│  [5] GPIO3                        GND [6] ├──┐   │
│  [7] GPIO4                    GPIO 14 [8] │  │   │
│  [9] GND                      GPIO 15[10] ├──│───│───┐
│ [11] GPIO17 ────────────┐    GPIO 18[12] │  │   │   │
│ [13] GPIO27             │           GND[14]│  │   │   │
│      ...                │                  │  │   │   │
│                         │                  │  │   │   │
└─────────────────────────┼──────────────────┘  │   │   │
                          │                     │   │   │
                          │  ┌──────────────────┘   │   │
                          │  │  ┌───────────────────┘   │
                          │  │  │  ┌────────────────────┘
                          │  │  │  │
                    ┌─────┴──┴──┴──┴─────┐
                    │  Momentary Button   │
                    │    with LED         │
                    │                     │
                    │  [Signal]  GPIO 17  │
                    │  [Ground]  GND      │
                    │  [LED +]   5V       │
                    │  [LED -]   GND      │
                    └─────────────────────┘
```

## Wire Color Recommendations

Use consistent colors to avoid confusion:

- **Red:** 5V Power
- **Black:** Ground (GND)
- **Yellow/White:** Signal (GPIO 17)
- **Blue:** 3.3V (if needed)

## Hardware Checklist

- [ ] Raspberry Pi Zero W 2
- [ ] microSD card (16GB+ recommended)
- [ ] Mini HDMI to HDMI cable
- [ ] 5V 2.5A power supply (micro USB)
- [ ] Momentary push button (with or without integrated LED)
- [ ] Jumper wires (female-to-female or female-to-male)
- [ ] Resistor (220-330Ω) if using separate LED
- [ ] Breadboard (optional, for prototyping)

## Testing the Wiring

1. **Before connecting power:**
   - Double-check all connections
   - Ensure no short circuits between 5V and GND
   - Verify button is connected to correct pins

2. **Visual inspection:**
   - LED should light up when powered (if using 5V LED)
   - No components should feel hot
   - All connections should be secure

3. **Software testing:**
   ```bash
   # Test GPIO input
   python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP); print('GPIO 17 state:', GPIO.input(17)); GPIO.cleanup()"
   ```

   Expected output:
   - Without button press: `GPIO 17 state: 1` (HIGH)
   - With button press: `GPIO 17 state: 0` (LOW)

## Troubleshooting

### LED not lighting up:
- Check 5V and GND connections
- Verify LED polarity
- Test LED with multimeter
- Check if button requires external power

### Button not responding:
- Verify GPIO 17 connection
- Check ground connection
- Test button continuity with multimeter
- Ensure button is normally-open (NO) type

### Intermittent operation:
- Check for loose connections
- Verify debounce setting (300ms default)
- Try different jumper wires
- Ensure good contact in breadboard (if using)

## Safety Notes

⚠️ **Important Safety Information:**

- Never connect 5V directly to GPIO pins (they are 3.3V tolerant only)
- Always use current-limiting resistors with LEDs
- Disconnect power before making wiring changes
- Avoid short circuits between power and ground
- Use proper wire gauge for current requirements
- Keep liquids away from electronics

## Additional Resources

- [Official Raspberry Pi GPIO Documentation](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header)
- [Raspberry Pi Pinout Interactive](https://pinout.xyz/)
- [RPi.GPIO Python Library Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
