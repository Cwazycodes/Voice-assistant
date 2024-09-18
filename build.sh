#!/usr/bin/env bash
# Install system dependencies
apt-get update && apt-get install -y portaudio19-dev libasound2-dev build-essential

# Install Python dependencies
pip install -r requirements.txt
