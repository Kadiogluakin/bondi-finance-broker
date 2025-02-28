# Bondi Finance AI Broker 🤖💼

An autonomous AI investment broker for Bondi Finance, specializing in tokenized corporate bonds. This broker leverages advanced AI to help democratize access to USD-denominated bonds through the Base blockchain, with integrated voice capabilities for direct investor engagement.

## Overview

Bondi Finance is revolutionizing the corporate bond market by making traditionally inaccessible USD bonds available to retail investors through tokenization. This AI broker serves as an autonomous agent that:

- Educates investors about tokenized bond opportunities
- Explains the benefits of the GLP bond (maturing June 2026)
- Guides users through the investment process
- Promotes the WHALE NFT tier benefits ($5,000+ investments)
- Handles investor questions and objections

The broker includes voice capabilities through ElevenLabs and Twilio integration, enabling direct phone conversations with potential investors.

### Key Features

Core Functionality:
- 🎯 Deep knowledge of Bondi Finance's tokenized bond offerings
- 💰 Strategic focus on converting $100 minimum investments to $5,000 WHALE NFT tier
- 🧠 Advanced understanding of bond markets, tokenization, and DeFi concepts
- 📊 Investment tracking and conversion monitoring

Voice Capabilities:
- 🎙️ ElevenLabs Conversational AI integration
- 📞 Twilio-powered outbound/inbound calls
- 🔄 Contextual conversation memory
- 🌐 Local testing via ngrok

## Prerequisites

- Python 3.7+
- ElevenLabs account with Conversational AI access
- Twilio account with active phone number
- ngrok account (for local development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bondi-finance-broker.git
cd bondi-finance-broker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
# Core AI Configuration
ELEVENLABS_XI_API_KEY=your_api_key
ELEVENLABS_AGENT_ID=your_agent_id
ELEVENLABS_VOICE_ID=your_voice_id

# Voice Integration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Development
NGROK_AUTH_TOKEN=your_auth_token
```

## Usage

1. Start the broker:
```bash
python bondi_finance_voice_calls.py
```

2. The broker will:
   - Initialize its knowledge base
   - Start the voice interaction server
   - Create required tunnels for webhooks
   - Present the operations menu

3. Available Operations:
   - Initiate calls to potential investors
   - Handle incoming investment inquiries
   - Track conversion metrics
   - Monitor funding progress

## Broker Configuration

### Core Knowledge Base
The broker maintains comprehensive knowledge of:
- Bondi Finance's tokenized bond platform
- GLP bond details and maturity schedule
- Bond market fundamentals
- Blockchain and DeFi concepts

### Investment Strategy
The broker is programmed to:
- Start with accessible $100 minimum investments
- Educate about OG NFT benefits
- Strategically promote WHALE NFT tier ($5,000+)
- Explain token airdrop potential
- Create urgency around the funding phase deadline

### Communication Approach
The broker maintains:
- Professional and educational tone
- Clear explanation of complex concepts
- Strategic urgency without pressure
- Adaptability to investor knowledge level

## Development

### Project Structure
```
bondi-finance-broker/
├── bondi_finance_voice_calls.py  # Main broker logic
├── requirements.txt              # Dependencies
├── .env                         # Configuration
├── .env.example                 # Config template
└── voice_calls.log             # Interaction logs
```

### Customization

1. Modify the broker's knowledge base:
```python
CHARACTER_DATA = {
    "name": "Bondi Finance Broker",
    "bio": [...],  # Core expertise
    "lore": [...], # Product knowledge
    "style": [...] # Communication style
}
```

2. Customize interaction patterns:
- `/incoming-call`: Initial engagement
- `/agent-response`: Main conversation logic
- `/agent-continue`: Follow-up handling

## Troubleshooting

Common issues and solutions:

1. **Knowledge Base Issues**
   - Update product information
   - Check market condition awareness

2. **Voice Integration**
   - Verify API configurations
   - Check audio format settings
   - Monitor connection stability

3. **Investment Tracking**
   - Verify funnel metrics
   - Monitor NFT qualification
   - Track funding phase progress

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
