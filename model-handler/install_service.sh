#!/bin/bash
# Service installation script for Model Switcher API

echo "Installing Model Switcher API service..."

# Check if we're running on a Raspberry Pi or Linux system
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
fi

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/model-switcher.service"
echo "Creating service file at $SERVICE_FILE"

# Check if python3 is available in the expected location
if [ ! -f "/home/pi/.local/bin/python3" ]; then
    echo "Warning: /home/pi/.local/bin/python3 not found. Using 'python3' command directly."
    PYTHON_PATH="python3"
else
    PYTHON_PATH="/home/pi/.local/bin/python3"
fi

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Model Switcher API Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pi-rag/model-handler
ExecStart=$PYTHON_PATH /home/pi/pi-rag/model-handler/main.py --host 0.0.0.0 --port 6006
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start at boot
echo "Enabling service to start at boot..."
sudo systemctl enable model-switcher.service

echo "Service installed successfully!"
echo ""
echo "You can now control the service with:"
echo "  sudo systemctl start model-switcher"
echo "  sudo systemctl stop model-switcher"
echo "  sudo systemctl restart model-switcher"
echo "  sudo systemctl status model-switcher"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u model-switcher -f"