# Bondi Finance Wolf Telegram Agent Setup Guide

## Current Status & Issues

1. **Character File**: Created at `/Users/akinkadioglu/bondi-broker/bondi-eliza/characters/bondi-broker.json`
2. **Configuration**: The agent is configured for Telegram integration and ElevenLabs voice capabilities
3. **Plugin Issues**: The required plugins are defined but not installed correctly
4. **Knowledge Processing Error**: The agent encounters a "RangeError: Invalid array length" error when processing character knowledge

## Required Components

### Core Plugins
- **Bootstrap Plugin** (`@elizaos/plugin-bootstrap`): Core functionality for conversation management
- **Node Plugin** (`@elizaos/plugin-node`): Enables voice synthesis and recognition
- **Coinbase Plugin** (`@elizaos/plugin-coinbase`): For investment processing and payments on the Base blockchain

### Telegram Integration
- **Telegram Client** (`@elizaos/client-telegram`): Required for Telegram bot functionality

## Step-by-Step Setup Guide

### 1. Fix Plugin Installation

```bash
# Navigate to the bondi-eliza directory
cd /Users/akinkadioglu/bondi-broker/bondi-eliza

# Install required plugins
pnpm add @elizaos/plugin-bootstrap @elizaos/plugin-node @elizaos/plugin-coinbase

# Install Telegram client
pnpm add @elizaos/client-telegram
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash

# ElevenLabs Voice Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=XPwgonYgvZVO8jPcWGpu
ELEVENLABS_MODEL_ID=eleven_turbo_v2
ELEVENLABS_STABILITY=0.6
ELEVENLABS_SIMILARITY_BOOST=0.8

# Coinbase Configuration (for blockchain transactions)
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_PRIVATE_KEY=your_coinbase_private_key
# The following will be generated automatically if not provided
# COINBASE_GENERATED_WALLET_HEX_SEED=
# COINBASE_GENERATED_WALLET_ID=
```

### 3. Fix Character File Knowledge Error

The "RangeError: Invalid array length" error likely occurs because of formatting issues in the knowledge array. Edit your character file:

```json
// In bondi-broker.json
{
  // ... existing configuration ...
  "knowledge": [
    "The global bond market is estimated to be between $100-130 trillion, comparable in size to both global GDP and the global equities market.",
    "Corporate bonds accounted for 34% of US corporate debt financing in 2023, up from 19% in 2000.",
    // ... other knowledge items ...
  ],
  // ... rest of configuration ...
}
```

Make sure there are no extremely long lines or malformed JSON structure.

### 4. Start the Agent with Increased Memory

```bash
cd /Users/akinkadioglu/bondi-broker/bondi-eliza
NODE_OPTIONS="--max-old-space-size=8192" pnpm start --characters="characters/bondi-broker.json"
```

## Telegram Bot Creation Process

1. Talk to [@BotFather](https://t.me/botfather) on Telegram
2. Use the `/newbot` command
3. Follow the prompts to create a new bot
4. Save the API token provided by BotFather
5. Add the token to your `.env` file

## Python Alternative Implementation

If the Eliza framework continues to have issues, you can use the Python-based implementation that was previously running. This implementation:

1. Was successfully running at `/Users/akinkadioglu/Downloads/twitter-bot/run_jordan_belfort.py`
2. Had active Telegram connections
3. Was using ElevenLabs for voice capabilities

To restart this implementation:

```bash
cd /Users/akinkadioglu/Downloads/twitter-bot/
python run_jordan_belfort.py
```

## Troubleshooting

### Memory Issues
If the agent crashes with "JavaScript heap out of memory", increase the Node.js memory limit:
```bash
NODE_OPTIONS="--max-old-space-size=16384" pnpm start --characters="characters/bondi-broker.json"
```

### Plugin Loading Errors
If plugins fail to load, check:
1. That they're installed correctly
2. That the plugin names in the character file match the installed packages
3. That the plugins are compatible with your Eliza version

### Telegram Connection Issues
If the Telegram bot doesn't connect:
1. Verify the bot token is correct
2. Ensure the bot has the required permissions
3. Check that the Telegram API credentials are valid 