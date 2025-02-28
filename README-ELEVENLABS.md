# Bondi Finance Wolf - ElevenLabs Voice Integration

This README provides instructions for setting up and testing the ElevenLabs voice integration for the Bondi Finance Wolf virtual broker.

## Overview

The Bondi Finance Wolf uses ElevenLabs' state-of-the-art voice technology to bring your virtual broker to life with dynamic, persuasive speech that embodies the Jordan Belfort-inspired sales persona. This README will guide you through the setup process and provide instructions for testing the integration.

## Quick Start

1. Make sure the `.env` file contains your ElevenLabs API key and other voice settings:

```
ELEVENLABS_XI_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=XPwgonYgvZVO8jPcWGpu
ELEVENLABS_MODEL_ID=eleven_turbo_v2
ELEVENLABS_STABILITY=0.6
ELEVENLABS_SIMILARITY_BOOST=0.8
ELEVENLABS_ENABLE_VOICE=true
```

2. Run the setup script to verify your configuration:

```bash
./setup-elevenlabs.sh
```

3. Start the Eliza server with your voice-enabled Bondi Finance Wolf:

```bash
cd bondi-eliza/eliza && pnpm start --characters="characters/bondi-broker.json"
```

4. Start the client interface:

```bash
cd bondi-eliza/eliza && pnpm start:client
```

5. Access the web interface at http://localhost:5174

## Standalone Voice Test

We've also included a standalone voice test page that allows you to test the ElevenLabs integration directly:

1. Access the voice test page at http://localhost:5174/voice-test.html
2. Enter your ElevenLabs API key
3. Enter your voice settings (or use the defaults)
4. Use one of the preset messages or enter your own
5. Click "Generate Speech" to hear how your message sounds with the Wolf's voice

## Customizing Voice Settings

The Wolf persona requires specific voice settings to maximize persuasiveness:

- **Stability (0.6)**: A lower stability creates more dynamic, emotional speech that varies in tone and emphasis, perfect for high-energy sales pitches.

- **Similarity Boost (0.8)**: A higher similarity boost maintains the distinctive character voice while allowing for natural expression.

You can adjust these settings in the `.env` file and in the character file (`bondi-broker.json`).

## Voice Integration Components

The ElevenLabs integration consists of several key components:

- **elevenlabs-config.js**: Configuration file for the ElevenLabs integration
- **test-elevenlabs.js**: Test script to verify the ElevenLabs integration
- **voice-config.js**: Custom voice configuration for the Eliza framework
- **voice-integration.js**: Client-side voice integration for the web interface
- **voice-test.html**: Standalone test page for the ElevenLabs integration

## Troubleshooting

If you encounter issues with the voice integration, try the following:

1. Verify that your ElevenLabs API key is correct
2. Ensure that the `ELEVENLABS_ENABLE_VOICE` setting is set to `true` in your `.env` file
3. Check that the voice ID is valid and accessible with your API key
4. Run the test script to diagnose any issues: `node test-elevenlabs.js`
5. Enable debugging: `DEBUG=eliza:voice,eliza:elevenlabs pnpm start`

## Additional Resources

- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [Voice Optimization Guide](https://elevenlabs.io/docs/speech-synthesis/voice-settings)
- [Eliza Voice Integration](https://docs.eliza.ai/integrations/voice)
- [Full ElevenLabs Integration Guide](./ELEVENLABS_INTEGRATION_GUIDE.md) 