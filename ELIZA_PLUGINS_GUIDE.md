# Eliza Plugins Implementation Guide for Bondi Finance Wolf

This guide provides detailed instructions for implementing and configuring essential Eliza plugins to enhance the capabilities of the Bondi Finance Wolf broker agent, particularly for aggressive sales tactics and investment processing.

## Table of Contents

1. [Overview of Selected Plugins](#overview-of-selected-plugins)
2. [Implementation Prerequisites](#implementation-prerequisites)
3. [Installation Instructions](#installation-instructions)
4. [Plugin-Specific Setup](#plugin-specific-setup)
5. [Feature Implementation Examples](#feature-implementation-examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Resources](#resources)

## Overview of Selected Plugins

The Bondi Finance Wolf integrates the following plugins to enhance its sales capabilities:

### 1. Bootstrap Plugin (`@eliza/plugin-bootstrap`)
- **Purpose**: Provides essential baseline functionality for the agent
- **Core Features**:
  - Conversation management
  - Context handling
  - Memory and state management
  - Basic text operations

### 2. Node Plugin (`@eliza/plugin-node`)
- **Purpose**: Enables advanced features requiring Node.js capabilities
- **Core Features**:
  - Voice synthesis and recognition
  - Web browsing and scraping
  - PDF document processing
  - File system operations

### 3. Coinbase Commerce Plugin (`@eliza/plugin-coinbase`)
- **Purpose**: Facilitates investment processing and payments
- **Core Features**:
  - Payment processing for investments
  - Transaction monitoring
  - Wallet integration
  - Payment confirmation

### 4. Image Generation Plugin (`@eliza/plugin-image-generation`)
- **Purpose**: Creates visual content for sales pitches
- **Core Features**:
  - Generate investment performance visuals
  - Create branded content
  - Produce NFT previews for WHALE and OG NFTs
  - Design sales materials

## Implementation Prerequisites

Before implementing the plugins, ensure you have:

1. **API Access**:
   - Coinbase Commerce account and API keys
   - OpenAI API key (for image generation)
   - ElevenLabs account and API key (for voice features)

2. **System Requirements**:
   - Node.js version 23 or higher
   - pnpm version 9 or higher
   - At least 4GB of available RAM
   - 2GB of free disk space

3. **Network Requirements**:
   - Reliable internet connection
   - Webhook endpoint accessibility (for payment notifications)

## Installation Instructions

### Step 1: Set Up Environment Variables

Create or modify your `.env` file to include the following variables:

```
# Core API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
ELEVENLABS_XI_API_KEY=your_elevenlabs_api_key

# Client Integration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Plugin Configuration
# Coinbase Plugin
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_PRIVATE_KEY=your_coinbase_private_key
COINBASE_COMMERCE_API_KEY=your_coinbase_commerce_api_key
COINBASE_NOTIFICATION_URI=your_webhook_url

# Image Generation Plugin
IMAGE_GENERATION_API_KEY=your_image_generation_api_key
```

### Step 2: Install Plugin Packages

```bash
# Navigate to your Eliza directory
cd eliza

# Install core plugins
pnpm add @eliza/plugin-bootstrap @eliza/plugin-node @eliza/plugin-coinbase @eliza/plugin-image-generation

# Install dependencies for Node plugin
pnpm add @google-cloud/text-to-speech @google-cloud/speech puppeteer pdf-parse sharp

# Build the project
pnpm build
```

### Step 3: Update Character Configuration

Modify your `characters/bondi-broker.json` file to include the plugins:

```json
{
  "name": "Bondi Finance Wolf",
  "modelProvider": "anthropic",
  "modelName": "claude-3-opus-20240229",
  "clientIntegration": {
    "telegram": {
      "botUsername": "BondiBrokerBot"
    }
  },
  "plugins": [
    "@eliza/plugin-bootstrap",
    "@eliza/plugin-node",
    "@eliza/plugin-coinbase",
    "@eliza/plugin-image-generation"
  ],
  // ... rest of character configuration
}
```

## Plugin-Specific Setup

### Bootstrap Plugin Setup

This plugin requires minimal configuration as it's enabled by default. Ensure your character JSON includes:

```json
"plugins": [
  "@eliza/plugin-bootstrap"
]
```

### Node Plugin Setup

1. **Voice Configuration**:
   
   Update your character file's voice section:

   ```json
   "voice": {
     "provider": "elevenlabs",
     "voiceId": "suitable_voice_id", 
     "stability": 0.6,
     "similarityBoost": 0.8,
     "style": 0.7,
     "useSpeakerBoost": true
   }
   ```

2. **Web Browsing Setup**:
   
   Ensure Puppeteer dependencies are installed:
   
   ```bash
   pnpm add puppeteer
   ```

3. **PDF Processing**:
   
   Enable PDF processing by installing required dependencies:
   
   ```bash
   pnpm add pdf-parse
   ```

### Coinbase Commerce Plugin Setup

1. **Create API Keys**:
   - Log in to [Coinbase Commerce](https://commerce.coinbase.com/)
   - Navigate to Settings > API Keys
   - Generate a new API key with read/write permissions
   - Add the key to your .env file

2. **Configure Webhooks**:
   - Set up a webhook endpoint in your Coinbase Commerce dashboard
   - Configure the webhook URL in your .env file as COINBASE_NOTIFICATION_URI
   - Ensure your webhook endpoint is publicly accessible

3. **Testing the Integration**:
   ```bash
   curl -X POST https://api.commerce.coinbase.com/charges \
     -H "X-CC-Api-Key: your_api_key" \
     -H "X-CC-Version: 2018-03-22" \
     -H "Content-Type: application/json" \
     -d '{"name":"Bondi Finance Investment","description":"Investment in btGLP Bond","pricing_type":"fixed_price","local_price":{"amount":"100.00","currency":"USD"}}'
   ```

### Image Generation Plugin Setup

1. **OpenAI Configuration**:
   - Ensure your OpenAI API key has access to DALL-E or other image generation capabilities
   - Add the key to your .env file

2. **Custom Prompts Setup**:
   
   Create image templates for bond investments:

   ```json
   "imagePrompts": {
     "whaleNft": "Professional, sleek image of a premium WHALE NFT for Bondi Finance, blue and gold color scheme, showing a whale swimming through a sea of bonds, corporate finance themed, white background, high detail",
     "ogNft": "Clean, modern image of an OG NFT for Bondi Finance investors, blue color scheme, showing a small bond certificate with 'OG' marked on it, financial theme, white background",
     "investmentChart": "Professional chart showing bond performance, upward trend, blue and green colors, clean corporate style, white background, labeled 'btGLP Bond Performance'"
   }
   ```

## Feature Implementation Examples

### 1. Voice Sales Pitch using Node Plugin

```javascript
// Example of how to trigger a voice response for sales pitch
const salesPitch = async (ctx) => {
  const pitch = "Listen, this btGLP bond is the HOTTEST opportunity in the market right now. You're getting GUARANTEED 13% APY while the traditional bonds are giving you what, 4-5%? That's NOTHING! Plus, with just a $5,000 investment, you get our exclusive WHALE NFT that guarantees future token airdrops. Don't miss this!";
  
  await ctx.speak(pitch, {
    voiceId: "your_selected_voice",
    stability: 0.6,
    similarityBoost: 0.8,
    style: 0.7
  });
};
```

### 2. Processing Investments with Coinbase Plugin

```javascript
// Example of creating a payment charge for investment
const createInvestment = async (ctx, amount) => {
  try {
    const charge = await ctx.plugins.coinbase.createCharge({
      name: "Bondi Finance btGLP Bond Investment",
      description: `Investment of $${amount} in btGLP Bond maturing June 2026`,
      pricing_type: "fixed_price",
      local_price: {
        amount: amount.toString(),
        currency: "USD"
      },
      metadata: {
        customer_id: ctx.userId,
        investment_type: amount >= 5000 ? "WHALE_NFT" : amount >= 100 ? "OG_NFT" : "STANDARD"
      }
    });
    
    return charge;
  } catch (error) {
    console.error("Failed to create investment charge:", error);
    throw error;
  }
};
```

### 3. Generating NFT Preview Images

```javascript
// Example of generating an NFT preview image
const generateNftPreview = async (ctx, investmentType) => {
  const prompt = investmentType === "WHALE" 
    ? ctx.character.imagePrompts.whaleNft
    : ctx.character.imagePrompts.ogNft;
  
  try {
    const image = await ctx.plugins.imageGeneration.generateImage({
      prompt,
      size: "1024x1024",
      quality: "hd"
    });
    
    return image;
  } catch (error) {
    console.error("Failed to generate NFT preview:", error);
    throw error;
  }
};
```

## Best Practices

### Voice Features (Node Plugin)

1. **Optimize Speech Patterns**:
   - Keep sales pitches under 30 seconds for maximum impact
   - Vary pace to emphasize key points (APY rates, NFT benefits)
   - Use the stability setting (0.6) to create more dynamic, assertive speech

2. **Web Browsing Best Practices**:
   - Use for real-time market data to enhance sales pitches
   - Process market news to create urgency ("market conditions are changing")
   - Limit concurrent browser instances to avoid memory issues

### Payment Processing (Coinbase Plugin)

1. **Investment Processing**:
   - Create tiered investment options ($100, $1000, $5000+)
   - Set appropriate expiration times for payment links (30-60 minutes)
   - Include clear metadata to track conversion sources

2. **Security Considerations**:
   - Never store private keys in your code
   - Implement webhook validation to prevent fraud
   - Use environment variables for all sensitive information

### Image Generation

1. **Visual Sales Materials**:
   - Generate charts showing historical bond performance
   - Create NFT previews that appear exclusive and valuable
   - Use consistent branding in all generated images

2. **Performance Optimization**:
   - Cache commonly used images to reduce API costs
   - Generate images at appropriate resolutions (512x512 for previews)
   - Implement rate limiting to avoid API throttling

## Troubleshooting

### Node Plugin Issues

| Issue | Solution |
|-------|----------|
| Voice synthesis fails | Check ElevenLabs API key and quota limits |
| Puppeteer crashes | Increase available memory or reduce concurrent browsers |
| PDF processing hangs | Check file size and implement timeout handling |

### Coinbase Plugin Issues

| Issue | Solution |
|-------|----------|
| API authentication errors | Verify API key permissions and expiration |
| Webhook not receiving events | Check URL accessibility and Coinbase webhook configuration |
| Payment links expire too quickly | Adjust expiration time in charge creation |

### Image Generation Issues

| Issue | Solution |
|-------|----------|
| Image generation fails | Verify API key and check content policy violations in prompts |
| Poor quality images | Refine prompts and specify higher resolution/quality |
| Rate limiting errors | Implement exponential backoff strategy for retries |

## Resources

### Official Documentation

- [Eliza Framework Documentation](https://elizaos.github.io/eliza/docs/)
- [Node Plugin Documentation](https://elizaos.github.io/eliza/plugins/node)
- [Coinbase Commerce API](https://commerce.coinbase.com/docs/)
- [OpenAI Image Generation API](https://platform.openai.com/docs/guides/images)

### Tutorials and Guides

- [Effective Voice Sales Techniques](https://elizaos.github.io/eliza/guides/voice-optimization)
- [Coinbase Commerce Integration Guide](https://elizaos.github.io/eliza/guides/payment-processing)
- [Creating Persuasive Visual Content](https://elizaos.github.io/eliza/guides/image-generation)

### Support Channels

- [Eliza Discord Community](https://discord.gg/eliza)
- [Coinbase Commerce Support](https://help.coinbase.com/en/commerce)
- [ElevenLabs Support](https://help.elevenlabs.io/) 