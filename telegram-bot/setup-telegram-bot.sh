# Check for required Python packages
pip install -r requirements.txt

# Check for ngrok
if ! command -v ngrok &> /dev/null; then
    echo "ngrok not found, installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install ngrok/ngrok/ngrok
    else
        # Linux/Windows (WSL)
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
        sudo apt update && sudo apt install ngrok
    fi
fi

# Start ngrok tunnel for Twilio
echo "Starting ngrok tunnel for Twilio webhook..."
ngrok http 5000 > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start and get URL
sleep 5
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo "ngrok tunnel started at $NGROK_URL"

# Update .env with ngrok URL
if grep -q "NGROK_URL" ../.env; then
    # Update existing NGROK_URL
    sed -i.bak "s|NGROK_URL=.*|NGROK_URL=$NGROK_URL|g" ../.env
else
    # Add NGROK_URL
    echo "NGROK_URL=$NGROK_URL" >> ../.env
fi

echo "Updated .env with ngrok URL"

# Load environment variables
if [ -f "../.env" ]; then
    echo "Loading environment variables from .env"
    source ../.env 