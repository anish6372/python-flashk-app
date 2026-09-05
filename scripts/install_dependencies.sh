#!/bin/bash

# Install dependencies script for AWS CodeDeploy
# This script runs after the application files are copied to the instance

set -e

echo "Starting dependency installation..."

# Update system packages
yum update -y

# Install Python 3.9 if not present
if ! command -v python3.9 &> /dev/null; then
    echo "Installing Python 3.9..."
    yum install -y python3.9 python3.9-pip
fi

# Create virtual environment if it doesn't exist
if [ ! -d "/opt/python-app/venv" ]; then
    echo "Creating Python virtual environment..."
    cd /opt/python-app
    python3.9 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
cd /opt/python-app
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install and configure nginx (optional)
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    amazon-linux-extras install -y nginx1
fi

# Set up application directory permissions
chown -R ec2-user:ec2-user /opt/python-app
chmod +x /opt/python-app/scripts/*.sh

# Create systemd service file
cat > /etc/systemd/system/python-app.service << EOF
[Unit]
Description=Python Flask Application
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/python-app
Environment=PATH=/opt/python-app/venv/bin
Environment=FLASK_ENV=production
ExecStart=/opt/python-app/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize new service
systemctl daemon-reload

echo "Dependencies installation completed successfully!"