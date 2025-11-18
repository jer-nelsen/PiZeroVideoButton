#!/usr/bin/env python3
"""
Raspberry Pi Zero Video Player with Button Control
Plays a video file on loop when button is pressed
Uses VLC with hardware acceleration for smooth playback
"""

import RPi.GPIO as GPIO
import subprocess
import time
import signal
import sys
import os

# Configuration
VIDEO_PATH = "/home/pi/video.mp4"
BUTTON_PIN = 17  # GPIO 17 (Physical Pin 11)
DEBOUNCE_TIME = 300  # milliseconds

# VLC player process
vlc_process = None
video_playing = False


def setup_gpio():
    """Initialize GPIO pins for button input"""
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(f"GPIO {BUTTON_PIN} configured as input with pull-up resistor")


def play_video():
    """Start video playback using VLC with hardware acceleration"""
    global vlc_process, video_playing

    # Stop any currently playing video
    stop_video()

    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file not found at {VIDEO_PATH}")
        return

    print(f"Starting video playback: {VIDEO_PATH}")

    # VLC command with hardware acceleration and HDMI audio
    # --play-and-exit: Exit after playing once
    # --fullscreen: Display in fullscreen
    # --no-osd: Disable on-screen display
    # --no-video-title-show: Don't show title
    # --aout=alsa: Use ALSA for audio
    # --alsa-audio-device=hdmi: Route audio to HDMI
    vlc_command = [
        "cvlc",  # Command-line VLC
        "--play-and-exit",
        "--fullscreen",
        "--no-osd",
        "--no-video-title-show",
        "--aout=alsa",
        "--alsa-audio-device=hdmi:CARD=vc4hdmi,DEV=0",
        "--vout=mmal_vout",  # Hardware accelerated video output for Pi
        "--codec=mmal_vcodec",  # Hardware accelerated video codec
        VIDEO_PATH
    ]

    try:
        vlc_process = subprocess.Popen(
            vlc_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        video_playing = True
        print("Video started successfully")

        # Monitor the process and update status when it ends
        def monitor_playback():
            global video_playing
            if vlc_process:
                vlc_process.wait()
                video_playing = False
                print("Video playback completed")

        # Start monitoring in background
        import threading
        monitor_thread = threading.Thread(target=monitor_playback, daemon=True)
        monitor_thread.start()

    except Exception as e:
        print(f"Error starting video: {e}")
        video_playing = False


def stop_video():
    """Stop video playback"""
    global vlc_process, video_playing

    if vlc_process and vlc_process.poll() is None:
        print("Stopping current video playback")
        vlc_process.terminate()
        try:
            vlc_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            vlc_process.kill()
        vlc_process = None

    video_playing = False


def button_callback(channel):
    """Handle button press event"""
    print("Button pressed - Starting video playback")
    play_video()


def signal_handler(sig, frame):
    """Handle program termination"""
    print("\nShutting down...")
    stop_video()
    GPIO.cleanup()
    sys.exit(0)


def main():
    """Main program loop"""
    print("=" * 50)
    print("Pi Zero Video Player with Button Control")
    print("=" * 50)
    print(f"Video file: {VIDEO_PATH}")
    print(f"Button pin: GPIO {BUTTON_PIN} (Physical Pin 11)")
    print("Press Ctrl+C to exit")
    print("=" * 50)

    # Check if video file exists
    if not os.path.exists(VIDEO_PATH):
        print(f"\nWARNING: Video file not found at {VIDEO_PATH}")
        print("Please update VIDEO_PATH in the script or place video.mp4 in /home/pi/")

    # Setup signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize GPIO
    setup_gpio()

    # Add button press event detection
    # Falling edge because we use pull-up resistor (button press pulls to ground)
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=button_callback,
        bouncetime=DEBOUNCE_TIME
    )

    print("\nSystem ready. Waiting for button press...")

    # Keep the program running
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
