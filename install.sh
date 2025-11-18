#!/bin/bash
#
# Installation script for Pi Zero Video Player with Button Control
# Run this script on your Raspberry Pi Zero W 2
#

set -e  # Exit on error

echo "========================================="
echo "Pi Zero Video Player - Installation"
echo "========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install required packages
echo ""
echo "Installing required packages..."
echo "This may take several minutes..."

# VLC with hardware acceleration support
sudo apt-get install -y vlc

# Python GPIO library
sudo apt-get install -y python3-rpi.gpio

# ALSA utilities for audio configuration
sudo apt-get install -y alsa-utils

echo ""
echo "Packages installed successfully!"

# Configure HDMI audio
echo ""
echo "Configuring HDMI audio..."

# Force HDMI audio output
if ! grep -q "hdmi_drive=2" /boot/config.txt; then
    echo "hdmi_drive=2" | sudo tee -a /boot/config.txt
    echo "Added hdmi_drive=2 to /boot/config.txt"
fi

# Set HDMI audio as default
sudo amixer cset numid=3 2 2>/dev/null || echo "ALSA audio configuration will be set on next boot"

# Create directory for video files
echo ""
echo "Setting up video directory..."
mkdir -p /home/pi/videos

# Copy Python script to home directory
echo ""
echo "Installing video player script..."
if [ -f "video_player.py" ]; then
    cp video_player.py /home/pi/video_player.py
    chmod +x /home/pi/video_player.py
    echo "video_player.py installed to /home/pi/"
else
    echo "Warning: video_player.py not found in current directory"
    echo "Please copy it manually to /home/pi/video_player.py"
fi

# Install systemd service
echo ""
echo "Installing systemd service..."
if [ -f "video-player.service" ]; then
    sudo cp video-player.service /etc/systemd/system/
    sudo systemctl daemon-reload
    echo "Systemd service installed"
else
    echo "Warning: video-player.service not found in current directory"
fi

# Ask user if they want to enable auto-start
echo ""
read -p "Enable auto-start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl enable video-player.service
    echo "Auto-start enabled"
else
    echo "Auto-start not enabled. You can enable it later with:"
    echo "  sudo systemctl enable video-player.service"
fi

# Check for video file
echo ""
if [ ! -f "/home/pi/video.mp4" ]; then
    echo "========================================="
    echo "IMPORTANT: No video file found!"
    echo "========================================="
    echo "Please copy your video file to:"
    echo "  /home/pi/video.mp4"
    echo ""
    echo "Or update VIDEO_PATH in /home/pi/video_player.py"
    echo "to point to your video file location"
else
    echo "Video file found at /home/pi/video.mp4"
fi

# Display wiring instructions
echo ""
echo "========================================="
echo "GPIO Wiring Instructions"
echo "========================================="
echo ""
echo "Button Connection:"
echo "  - Button Signal -> GPIO 17 (Physical Pin 11)"
echo "  - Button Ground -> Ground (Physical Pin 9)"
echo ""
echo "LED Connection (if separate):"
echo "  - LED Positive -> 5V (Physical Pin 2)"
echo "  - LED Negative -> Ground (Physical Pin 6)"
echo "  - Use appropriate resistor (typically 220-330Ω)"
echo ""
echo "Note: The internal pull-up resistor is enabled"
echo "on GPIO 17, so no external resistor needed"
echo "for the button signal."
echo ""

# Installation complete
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Copy your video.mp4 file to /home/pi/"
echo "2. Connect your button to GPIO 17 (Pin 11) and Ground (Pin 9)"
echo "3. Connect LED to 5V (Pin 2) and Ground (Pin 6) with resistor"
echo "4. Reboot your Pi or start the service manually:"
echo "   sudo systemctl start video-player.service"
echo ""
echo "To view logs:"
echo "   sudo journalctl -u video-player.service -f"
echo ""
echo "To test without auto-start:"
echo "   python3 /home/pi/video_player.py"
echo ""
