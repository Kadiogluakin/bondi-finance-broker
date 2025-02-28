#!/bin/bash

# Set up error handling
set -e
trap cleanup EXIT

# Function to clean up processes on exit
function cleanup {
    echo "Stopping services..."
    if [ -n "$FLASK_PID" ]; then
        kill $FLASK_PID 2>/dev/null || true
    fi
    if [ -n "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null || true
        pkill -f ngrok || true
    fi
    echo "All services stopped"
}

# Ensure we're in the telegram-bot directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment in current directory..."
    source venv/bin/activate
elif [ -d "../venv" ]; then
    echo "Activating virtual environment in parent directory..."
    source ../venv/bin/activate
else
    echo "WARNING: No virtual environment found. Using system Python."
fi

# Verify Python is available
if ! command -v python >/dev/null 2>&1; then
    echo "ERROR: Python not found. Make sure Python is installed and available in PATH."
    exit 1
fi

# Start ngrok tunnel for Twilio webhook
echo "Starting ngrok tunnel for Twilio webhook..."
pkill -f ngrok 2>/dev/null || true

# Start ngrok and capture its PID
ngrok http 5000 > ngrok.log 2>&1 &
NGROK_PID=$!
echo "Started ngrok with PID: $NGROK_PID"

# Wait for ngrok to start
echo "Waiting for ngrok to start (10 seconds)..."
sleep 10

# Get ngrok URL - make sure to handle errors
if curl -s http://localhost:4040/api/tunnels >/dev/null 2>&1; then
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
    
    if [ -z "$NGROK_URL" ] || [ "$NGROK_URL" = "null" ]; then
        echo "ERROR: Could not extract ngrok URL. Check ngrok.log for details."
        cat ngrok.log
        exit 1
    fi
    
    echo "ngrok tunnel started at $NGROK_URL"
    
    # Update .env with ngrok URL (in parent directory)
    ENV_FILE="../.env"
    if [ -f "$ENV_FILE" ]; then
        # Fix the TWILIO_PHONE_NUMBER line if needed
        if grep -q "TWILIO_PHONE_NUMBER=.*NGROK_URL=" "$ENV_FILE"; then
            sed -i.bak "s/\(TWILIO_PHONE_NUMBER=.*\)NGROK_URL=.*/\1/" "$ENV_FILE"
            echo "Fixed .env format for TWILIO_PHONE_NUMBER."
        fi
        
        # Update or add NGROK_URL
        if grep -q "NGROK_URL=" "$ENV_FILE"; then
            sed -i.bak "s|NGROK_URL=.*|NGROK_URL=$NGROK_URL|" "$ENV_FILE"
        else
            echo "" >> "$ENV_FILE"  # Ensure there's a newline
            echo "NGROK_URL=$NGROK_URL" >> "$ENV_FILE"
        fi
        echo "Updated .env with ngrok URL: $NGROK_URL"
    else
        echo "ERROR: .env file not found at $ENV_FILE"
        exit 1
    fi
else
    echo "ERROR: ngrok API not available. Check if ngrok started correctly."
    cat ngrok.log
    exit 1
fi

# Start Flask server for Twilio webhooks in the background
echo "Starting Flask server for Twilio webhooks..."
python bondi_finance_voice_calls.py > twilio_server.log 2>&1 &
FLASK_PID=$!

# Wait for Flask server to start
sleep 5
echo "Flask server started with PID: $FLASK_PID"

# Check if Flask server started successfully
if ! ps -p $FLASK_PID > /dev/null; then
    echo "ERROR: Flask server failed to start. Check twilio_server.log for details:"
    cat twilio_server.log
    exit 1
fi

# Start Telegram bot
echo "Starting Telegram bot..."
python telegram_voice_client_with_calls.py 