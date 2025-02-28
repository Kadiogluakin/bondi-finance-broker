#!/bin/bash

# Setup script for ElevenLabs integration with Bondi Finance Wolf
echo "====================================================="
echo "Setting up ElevenLabs voice for Bondi Finance Wolf..."
echo "====================================================="

# Check for .env file
if [ ! -f .env ]; then
  echo "❌ .env file not found. Please create a .env file with your configuration."
  exit 1
fi

# Source environment variables
source .env

# Check for required environment variables
if [ -z "$ELEVENLABS_XI_API_KEY" ]; then
  echo "❌ ELEVENLABS_XI_API_KEY is not set in .env file"
  exit 1
fi

# Install required dependencies
echo "📦 Installing required dependencies..."
npm install axios dotenv fs-extra

# Check if the specified voice ID is set
VOICE_ID=${ELEVENLABS_VOICE_ID:-"XPwgonYgvZVO8jPcWGpu"}
echo "🎙️ Using voice ID: $VOICE_ID"

# Check if the model ID is set
MODEL_ID=${ELEVENLABS_MODEL_ID:-"eleven_turbo_v2"}
echo "🧠 Using model ID: $MODEL_ID"

# Validate voice settings
STABILITY=${ELEVENLABS_STABILITY:-"0.6"}
SIMILARITY_BOOST=${ELEVENLABS_SIMILARITY_BOOST:-"0.8"}
echo "⚙️ Voice stability: $STABILITY"
echo "⚙️ Voice similarity boost: $SIMILARITY_BOOST"

# Run voice test
echo "🔊 Testing voice integration..."
node test-elevenlabs.js

# Check if test was successful
if [ $? -eq 0 ]; then
  echo "✅ ElevenLabs voice integration test successful!"
  echo ""
  echo "Voice is configured for \"Bondi Finance Wolf\" with the following settings:"
  echo "- Voice ID: $VOICE_ID"
  echo "- Model ID: $MODEL_ID"
  echo "- Stability: $STABILITY"
  echo "- Similarity Boost: $SIMILARITY_BOOST"
  echo ""
  echo "Audio test saved to audio-tests/bondi-wolf-test.mp3"
  echo ""
  echo "To start using your voice-enabled broker:"
  echo "1. Copy characters/bondi-broker.json to your Eliza characters directory"
  echo "2. Start Eliza: cd bondi-eliza/eliza && pnpm start --characters=\"characters/bondi-broker.json\""
  echo "3. Start the client: cd bondi-eliza/eliza && pnpm start:client"
  echo "4. Access the web interface at http://localhost:5173/"
else
  echo "❌ ElevenLabs voice integration test failed. Please check the error messages above."
  exit 1
fi

exit 0 