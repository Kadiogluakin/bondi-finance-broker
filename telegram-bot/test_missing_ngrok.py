#!/usr/bin/env python3
"""Test script for when NGROK_URL is not set."""

import os
import sys
import subprocess

# Unset NGROK_URL in the environment
os.environ["NGROK_URL"] = ""

# Print a message
print("Testing without NGROK_URL...")
print("=" * 40)

# Call the check_twilio_and_ngrok_status function directly
from telegram_voice_client_with_calls import check_twilio_and_ngrok_status

# Check status
status, message = check_twilio_and_ngrok_status()
print(f"Status: {status}")
print(f"Message: {message}")
print("=" * 40)

# Exit
print("Test completed.") 