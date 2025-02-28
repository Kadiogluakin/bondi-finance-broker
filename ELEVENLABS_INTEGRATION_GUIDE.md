# ElevenLabs Integration Guide for Bondi Finance Wolf

This guide explains how to set up and use ElevenLabs voice technology with your Bondi Finance Wolf virtual broker for high-impact sales conversations.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Voice Optimization for Sales](#voice-optimization-for-sales)
- [Testing Your Integration](#testing-your-integration)
- [Troubleshooting](#troubleshooting)

## Overview

The Bondi Finance Wolf uses ElevenLabs' state-of-the-art voice technology to bring your virtual broker to life with dynamic, persuasive speech that embodies the Jordan Belfort-inspired sales persona. This integration enables:

- Real-time voice responses in the web interface
- Voice message capabilities on Telegram
- Natural, high-energy delivery for maximum sales impact
- Dynamic expression that varies based on sales context

## Prerequisites

Before you begin, ensure you have:

1. An ElevenLabs account (sign up at [elevenlabs.io](https://elevenlabs.io))
2. Your ElevenLabs API key (found in your ElevenLabs dashboard)
3. A selected voice ID (or use our recommended voice for the Wolf persona)
4. The Eliza framework properly installed

## Configuration

### 1. Environment Variables

The following environment variables must be set in your `.env` file:

```
# Core ElevenLabs Settings
ELEVENLABS_XI_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# Optional Advanced Settings
ELEVENLABS_MODEL_ID=eleven_turbo_v2
ELEVENLABS_STABILITY=0.6
ELEVENLABS_SIMILARITY_BOOST=0.8
ELEVENLABS_ENABLE_VOICE=true
```

### 2. Character File Configuration

Your `bondi-broker.json` character file should include these voice settings:

```json
"settings": {
  "voice": { 
    "provider": "elevenlabs",
    "voiceId": "XPwgonYgvZVO8jPcWGpu",
    "stability": 0.6,
    "similarity_boost": 0.8
  }
}
```

### 3. Running the Setup Script

Execute the provided setup script to install dependencies and verify your configuration:

```bash
./setup-elevenlabs.sh
```

## Voice Optimization for Sales

The Wolf persona requires specific voice settings to maximize persuasiveness:

### Recommended Settings

- **Stability (0.6)**: A lower stability creates more dynamic, emotional speech that varies in tone and emphasis, perfect for high-energy sales pitches.

- **Similarity Boost (0.8)**: A higher similarity boost maintains the distinctive character voice while allowing for natural expression.

### Context-Based Voice Patterns

Our integration includes contextual voice patterns that automatically adjust based on the sales situation:

1. **Pitch Mode**: Higher energy, faster pace when introducing investment opportunities
2. **Objection Handling**: Confident, steady tone with authoritative emphasis
3. **Closing Mode**: Slightly slower, more deliberate speech with urgency cues

## Testing Your Integration

Use our test script to verify your ElevenLabs integration:

```bash
node test-elevenlabs.js
```

This will:
1. Check your API key and connection
2. Generate a sample sales pitch audio file
3. Save the result to the `audio-tests` directory for your review

## Interactive Testing

To test the voice in action:

1. Start the Eliza server:
   ```bash
   cd bondi-eliza/eliza && pnpm start --characters="characters/bondi-broker.json"
   ```

2. Start the client interface:
   ```bash
   cd bondi-eliza/eliza && pnpm start:client
   ```

3. Navigate to http://localhost:5174 in your browser
4. Interact with the Bondi Finance Wolf and experience the voice responses

## Troubleshooting

### Common Issues

1. **No voice output**
   - Verify your API key is correct
   - Check that voice is enabled in the character file
   - Ensure your browser allows audio playback

2. **Latency Issues**
   - Use the `eleven_turbo_v2` model for faster responses
   - Consider implementing sentence splitting for smoother delivery

3. **Voice Quality Issues**
   - Adjust stability and similarity_boost parameters
   - Try different voice IDs from your ElevenLabs collection

### Logs and Diagnostics

Enable debugging to get more information:

```
DEBUG=eliza:voice,eliza:elevenlabs pnpm start
```

## Additional Resources

- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [Voice Optimization Guide](https://elevenlabs.io/docs/speech-synthesis/voice-settings)
- [Eliza Voice Integration](https://docs.eliza.ai/integrations/voice) 