# Pi Zero Video Button Controller

A complete solution for turning a Raspberry Pi Zero W 2 into a video playback device with button control. Perfect for interactive displays, exhibits, presentations, or any project requiring video playback triggered by a physical button.

## Features

- ✅ Hardware-accelerated video playback with VLC
- ✅ Button-controlled video restart
- ✅ HDMI audio output
- ✅ Auto-start on boot (optional)
- ✅ Plays video once and pauses on last frame
- ✅ Clean GPIO handling with debouncing
- ✅ Easy installation and configuration

## Hardware Requirements

- **Raspberry Pi Zero W 2**
- **microSD Card:** 16GB or larger (Class 10 recommended)
- **Power Supply:** 5V 2.5A micro USB
- **Video Output:** Mini HDMI to HDMI cable
- **Button:** Momentary push button (normally open)
- **LED (Optional):** Built-in button LED or separate LED with 220-330Ω resistor
- **Wiring:** Jumper wires (female-to-female recommended)

## Software Requirements

- Raspberry Pi OS Lite or Desktop (Bullseye or later)
- VLC media player
- Python 3
- RPi.GPIO library

## Quick Start

### 1. Prepare Your Raspberry Pi

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install git
sudo apt-get install -y git

# Clone this repository
git clone https://github.com/yourusername/PiZeroVideoButton.git
cd PiZeroVideoButton
```

### 2. Run Installation Script

```bash
chmod +x install.sh
./install.sh
```

The installation script will:
- Install VLC with hardware acceleration
- Install Python GPIO library
- Configure HDMI audio output
- Set up the systemd service
- Optionally enable auto-start on boot

### 3. Add Your Video

Copy your video file to the Pi:

```bash
# Option 1: Using scp from another computer
scp your-video.mp4 pi@raspberrypi.local:/home/pi/video.mp4

# Option 2: Direct copy on the Pi
cp /path/to/your/video.mp4 /home/pi/video.mp4
```

**Supported video formats:** MP4, AVI, MKV, MOV (H.264 codec recommended for best performance)

### 4. Wire Your Button

See [WIRING.md](WIRING.md) for detailed wiring instructions.

**Quick reference:**
- Button Signal → GPIO 17 (Physical Pin 11)
- Button Ground → Ground (Physical Pin 9)
- LED Power → 5V (Physical Pin 2)
- LED Ground → Ground (Physical Pin 6)

### 5. Start the Service

```bash
# Start immediately
sudo systemctl start video-player.service

# Enable auto-start on boot
sudo systemctl enable video-player.service

# Check status
sudo systemctl status video-player.service
```

## Configuration

### Change Video File Path

Edit the Python script:

```bash
nano /home/pi/video_player.py
```

Change this line:
```python
VIDEO_PATH = "/home/pi/video.mp4"
```

### Change GPIO Pin

Edit the Python script to use a different GPIO pin:

```python
BUTTON_PIN = 17  # Change to your desired GPIO number
```

Remember to update your wiring accordingly!

### Adjust Button Debounce Time

If you experience multiple triggers from a single button press:

```python
DEBOUNCE_TIME = 300  # Increase this value (in milliseconds)
```

## Usage

### Manual Testing

Test the script without auto-start:

```bash
python3 /home/pi/video_player.py
```

Press Ctrl+C to exit.

### Service Management

```bash
# Start service
sudo systemctl start video-player.service

# Stop service
sudo systemctl stop video-player.service

# Restart service
sudo systemctl restart video-player.service

# Enable auto-start
sudo systemctl enable video-player.service

# Disable auto-start
sudo systemctl disable video-player.service

# View logs
sudo journalctl -u video-player.service -f
```

## How It Works

1. **Boot:** System starts and optionally launches the video player service
2. **Ready:** Script waits for button press, monitoring GPIO 17
3. **Button Press:** When button is pressed (GPIO pulled to ground):
   - Video player starts with hardware acceleration
   - Video plays at native framerate with HDMI audio
   - Video plays once and pauses on last frame
4. **Repeat:** Subsequent button presses restart the video

## GPIO Pin Configuration

The script uses:
- **GPIO Mode:** BCM numbering
- **Pin 17:** Input with internal pull-up resistor enabled
- **Trigger:** Falling edge (button press pulls pin to ground)
- **Debounce:** 300ms to prevent multiple triggers

## Video Player Settings

VLC is configured with:
- **Hardware acceleration:** MMAL (Broadcom multimedia abstraction layer)
- **Audio output:** ALSA with HDMI routing
- **Display:** Fullscreen with no OSD
- **Playback:** Play once and exit

## Troubleshooting

### Video doesn't play

**Check video file:**
```bash
ls -lh /home/pi/video.mp4
```

**Test VLC manually:**
```bash
cvlc --play-and-exit /home/pi/video.mp4
```

**Check service logs:**
```bash
sudo journalctl -u video-player.service -n 50
```

### No audio on HDMI

**Force HDMI audio in config:**
```bash
sudo nano /boot/config.txt
```

Add or verify:
```
hdmi_drive=2
```

**Set HDMI as default audio:**
```bash
sudo amixer cset numid=3 2
```

Reboot after changes:
```bash
sudo reboot
```

### Button not responding

**Test GPIO input:**
```bash
python3 << EOF
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press button (Ctrl+C to exit)...")
try:
    while True:
        print(f"GPIO 17 state: {GPIO.input(17)}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
EOF
```

Expected: Shows `1` normally, `0` when button is pressed

**Check wiring:**
- Verify GPIO 17 connection (Physical Pin 11)
- Verify ground connection (Physical Pin 9)
- Test button continuity with multimeter

### Video playback is choppy

**Update firmware:**
```bash
sudo rpi-update
sudo reboot
```

**Optimize video file:**
- Use H.264 codec
- Reduce resolution if necessary (720p works well on Pi Zero)
- Reduce bitrate (2-4 Mbps recommended)

**Convert video with ffmpeg:**
```bash
ffmpeg -i input.mp4 -c:v h264_omx -b:v 2M -c:a aac output.mp4
```

### Service won't start on boot

**Check service status:**
```bash
sudo systemctl status video-player.service
```

**Check if enabled:**
```bash
sudo systemctl is-enabled video-player.service
```

**Re-enable if needed:**
```bash
sudo systemctl enable video-player.service
sudo systemctl daemon-reload
```

## Performance Optimization

### For best performance on Pi Zero:

1. **Use Raspberry Pi OS Lite** (no desktop environment)
2. **Optimize video encoding:**
   - Codec: H.264
   - Resolution: 720p or lower
   - Bitrate: 2-4 Mbps
   - Frame rate: 24-30 fps

3. **Disable unnecessary services:**
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

4. **Overclock (optional, at your own risk):**
```bash
sudo nano /boot/config.txt
```

Add:
```
arm_freq=1000
gpu_mem=128
```

## Advanced Configuration

### Multiple Button Support

To add more buttons for different videos, modify the script:

```python
BUTTON1_PIN = 17
BUTTON2_PIN = 27
VIDEO1_PATH = "/home/pi/video1.mp4"
VIDEO2_PATH = "/home/pi/video2.mp4"

def button1_callback(channel):
    play_video(VIDEO1_PATH)

def button2_callback(channel):
    play_video(VIDEO2_PATH)

GPIO.add_event_detect(BUTTON1_PIN, GPIO.FALLING, callback=button1_callback, bouncetime=300)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.FALLING, callback=button2_callback, bouncetime=300)
```

### Loop Video Continuously

To loop video without pause:

Change VLC command to:
```python
vlc_command = [
    "cvlc",
    "--loop",  # Add this
    "--fullscreen",
    # ... rest of options
]
```

### Add LED Control

To control an LED via GPIO (in addition to button LED):

```python
LED_PIN = 18  # Choose your pin

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Off initially

def play_video():
    GPIO.output(LED_PIN, GPIO.HIGH)  # LED on while playing
    # ... existing code ...

def stop_video():
    # ... existing code ...
    GPIO.output(LED_PIN, GPIO.LOW)  # LED off when stopped
```

## Project Structure

```
PiZeroVideoButton/
├── README.md              # This file
├── WIRING.md             # Detailed wiring guide
├── video_player.py       # Main Python script
├── video-player.service  # Systemd service file
└── install.sh           # Installation script
```

## File Locations on Pi

After installation:
- Script: `/home/pi/video_player.py`
- Service: `/etc/systemd/system/video-player.service`
- Video: `/home/pi/video.mp4` (or your custom path)
- Logs: View with `journalctl -u video-player.service`

## Technical Details

### Power Consumption
- Typical: 200-400mA during playback
- Recommend 2.5A power supply for stability

### Boot Time
- From power on to ready: ~30-45 seconds
- From power on to video playing: ~35-50 seconds (if auto-start enabled)

### Supported Video Codecs
- **Best:** H.264/AVC (hardware accelerated)
- **Supported:** MPEG-4, H.265/HEVC (may be slower)
- **Audio:** AAC, MP3, AC3

## FAQ

**Q: Can I use this with other Raspberry Pi models?**
A: Yes! Works with all Raspberry Pi models. Pi 3 and 4 will have better performance.

**Q: Can I play videos from a USB drive?**
A: Yes, mount the USB drive and update VIDEO_PATH to point to it.

**Q: Does this work with Raspberry Pi OS Desktop?**
A: Yes, but OS Lite is recommended for better performance.

**Q: Can I add a power button to safely shut down?**
A: Yes, you can add another GPIO button that triggers `sudo shutdown -h now`.

**Q: How do I change the video without SSH?**
A: Replace video.mp4 on the microSD card using another computer, or use a USB drive.

**Q: Can I use a touchscreen instead of a button?**
A: Yes, modify the script to detect touch events instead of GPIO input.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is released under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review [WIRING.md](WIRING.md) for wiring issues
- Open an issue on GitHub

## Credits

Created for Raspberry Pi Zero W 2 video button control projects.

## Changelog

### Version 1.0.0
- Initial release
- VLC-based playback with hardware acceleration
- Single button control
- Auto-start support
- HDMI audio configuration
- Comprehensive documentation

---

**Enjoy your Pi Zero Video Button Controller!** 🎬
