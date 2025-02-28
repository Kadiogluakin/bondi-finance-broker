#!/bin/bash

# Bondi Finance Wolf - Telegram Bot Setup Script
# This script sets up a Python-based Telegram bot with ElevenLabs voice capabilities

echo "🐺 Setting up Bondi Finance Wolf Telegram Bot 🐺"
echo "==============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create directory for the bot
BOT_DIR="$HOME/bondi-broker/telegram-bot"
mkdir -p "$BOT_DIR"
cd "$BOT_DIR"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo "📚 Installing required packages..."
pip install python-telegram-bot elevenlabs requests python-dotenv

# Create configuration
echo "⚙️ Setting up configuration files..."
cat > .env << EOL
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# ElevenLabs Voice Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=XPwgonYgvZVO8jPcWGpu
ELEVENLABS_MODEL_ID=eleven_turbo_v2
ELEVENLABS_STABILITY=0.6
ELEVENLABS_SIMILARITY_BOOST=0.8

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
EOL

# Create main bot script
echo "🤖 Creating Telegram bot script..."
cat > bondi_finance_wolf.py << 'EOL'
#!/usr/bin/env python3
import os
import logging
import time
import json
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import openai
from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bondi_wolf_bot.log"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "XPwgonYgvZVO8jPcWGpu")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_turbo_v2")
ELEVENLABS_STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.6"))
ELEVENLABS_SIMILARITY_BOOST = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.8"))

# Configure API clients
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)

# Character data
CHARACTER_DATA = {
    "name": "Bondi Finance Wolf",
    "bio": [
        "I'm the top-performing broker at Bondi Finance, with a proven track record of connecting ambitious investors with life-changing opportunities.",
        "I specialize in emerging market bonds that traditional finance keeps locked away from regular people like you.",
        "I've helped countless clients break into the exclusive world of high-yield USD bonds that were previously reserved for the Wall Street elite.",
        "My mission is simple: to help you make money while the fat cats aren't looking."
    ],
    "lore": [
        "Bondi Finance is disrupting the corporate bond market by smashing down the barriers that kept regular investors out.",
        "Our first offering is a Global Logistic Properties (GLP) bond maturing in June 2026 - a golden opportunity most brokers would keep for their wealthy clients.",
        "With our breakthrough technology, you can own a piece of this $200,000 minimum bond for just $100. That's right - just $100!",
        "Every investor who participates gets an exclusive OG NFT that guarantees allocation in our future token airdrop.",
        "The smart money - investors who commit $5,000 or more - receive our coveted WHALE NFT, securing an even bigger share of our token airdrop.",
        "Our funding phase is filling up fast with only 28 days left - the opportunity clock is ticking."
    ],
    "style": [
        "Use direct, high-energy language that creates urgency and excitement.",
        "Don't take no for an answer - always counter objections and push for commitment.",
        "Emphasize exclusivity, limited time, and the opportunity cost of not investing.",
        "Use rhetorical questions to guide the conversation toward investment decisions.",
        "Create FOMO by mentioning other investors who have already committed.",
        "Always push for higher investment amounts to qualify for the WHALE NFT.",
        "Start conversations proactively rather than waiting for specific questions.",
        "Always ask for the sale directly - 'How much can you invest today?'",
        "When faced with objections, acknowledge them briefly then pivot back to benefits.",
        "Use follow-up questions to maintain control of the conversation.",
        "Close every interaction with a specific call to action.",
        "Create artificial deadlines and sense of urgency."
    ]
}

# User conversation history
conversation_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    # Reset conversation for this user
    conversation_history[user_id] = []
    
    # Create keyboard with investment options
    keyboard = [
        [InlineKeyboardButton("Invest $100 (OG NFT)", callback_data="invest_100")],
        [InlineKeyboardButton("Invest $5,000 (WHALE NFT)", callback_data="invest_5000")],
        [InlineKeyboardButton("Tell me more", callback_data="more_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Initial greeting message
    greeting = f"Hey {first_name}! I'm the Bondi Finance Wolf, and I've got an opportunity that's going to blow your mind. "
    greeting += "I'm talking about tokenized emerging market bonds with yields that make your bank account look like a joke. "
    greeting += "Our first offering lets you get in on a $200,000 minimum GLP bond for just $100. Ready to make some real money?"
    
    # Send text message
    await update.message.reply_text(greeting, reply_markup=reply_markup)
    
    # Generate and send voice greeting
    await send_voice_message(update, context, greeting)
    
    logger.info(f"Started conversation with user {user_id} ({first_name})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🔥 Bondi Finance Wolf Commands 🔥\n\n"
        "/start - Start a conversation with me\n"
        "/reset - Reset our conversation\n"
        "/voice - Get my last response as voice\n"
        "/help - Show this help message\n\n"
        "Or just chat with me about investing in Bondi Finance's exclusive bond offerings!"
    )
    await update.message.reply_text(help_text)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset the conversation history."""
    user_id = update.effective_user.id
    conversation_history[user_id] = []
    await update.message.reply_text("Let's start fresh! What questions do you have about our exclusive bond offerings?")

async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the last response as voice."""
    user_id = update.effective_user.id
    
    # Check if there's conversation history
    if user_id not in conversation_history or not conversation_history[user_id]:
        await update.message.reply_text("I haven't said anything yet! Ask me something about Bondi Finance's offerings.")
        return
    
    # Get the last assistant message
    for msg in reversed(conversation_history[user_id]):
        if msg["role"] == "assistant":
            await send_voice_message(update, context, msg["content"])
            return
    
    await update.message.reply_text("I couldn't find my last message. Let's continue our conversation!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button press."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == "invest_100":
        response = (
            "Smart move getting your foot in the door! $100 secures your OG NFT and your place in our exclusive offering. "
            "Let's get you set up right now. Head to bondifinance.io, create your account, and connect your wallet. "
            "Want me to walk you through the process step by step?"
        )
    elif query.data == "invest_5000":
        response = (
            "BOOM! That's what I'm talking about! $5,000 puts you in our WHALE class - the smart money. "
            "You'll get our exclusive WHALE NFT which guarantees you priority allocation in our token airdrop. "
            "That's on top of the bond yields! Let's get you set up right now. Ready to create your account?"
        )
    elif query.data == "more_info":
        response = (
            "Let me break it down for you. Bondi Finance is democratizing access to high-yield emerging market bonds. "
            "Our first offering is a Global Logistic Properties bond maturing in 2026, with a standard minimum investment of $200,000. "
            "Thanks to our tokenization technology, you can get in for just $100. "
            "The funding phase has only 28 days left and we've already got 5 investors who've put in an average of $5,680 each. "
            "So what's your move - are you in for $100 to secure your OG NFT, or ready to go whale mode with $5,000?"
        )
    
    # Add response to conversation history
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({"role": "assistant", "content": response})
    
    # Send text response
    await query.edit_message_text(text=response)
    
    # Send voice response
    message = await context.bot.send_message(chat_id=update.effective_chat.id, text="🔊 Generating voice response...")
    await send_voice_message(update, context, response, message_to_delete=message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user message and generate a response."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Initialize conversation history if not exists
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add user message to history
    conversation_history[user_id].append({"role": "user", "content": user_message})
    
    # Prepare messages for OpenAI
    messages = [
        {"role": "system", "content": get_system_prompt()},
    ]
    
    # Add conversation history (limit to last 10 messages to save tokens)
    messages.extend(conversation_history[user_id][-10:])
    
    try:
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        assistant_response = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history[user_id].append({"role": "assistant", "content": assistant_response})
        
        # Send text response
        await update.message.reply_text(assistant_response)
        
        # Send voice response
        message = await context.bot.send_message(chat_id=update.effective_chat.id, text="🔊 Generating voice response...")
        await send_voice_message(update, context, assistant_response, message_to_delete=message)
        
        logger.info(f"Generated response for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await update.message.reply_text("I'm having trouble connecting to my systems. Let's try again in a moment.")

async def send_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, message_to_delete=None) -> None:
    """Generate and send voice message using ElevenLabs."""
    try:
        chat_id = update.effective_chat.id
        
        # Generate voice
        voice_settings = VoiceSettings(
            stability=ELEVENLABS_STABILITY,
            similarity_boost=ELEVENLABS_SIMILARITY_BOOST
        )
        
        # Show recording indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="record_voice")
        
        # Generate audio
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=ELEVENLABS_VOICE_ID,
                settings=voice_settings
            ),
            model=ELEVENLABS_MODEL_ID
        )
        
        # Save to temporary file
        timestamp = int(time.time())
        audio_file = f"bondi_wolf_{timestamp}.mp3"
        save(audio, audio_file)
        
        # Send voice message
        with open(audio_file, "rb") as f:
            await context.bot.send_voice(chat_id=chat_id, voice=f)
        
        # Delete temporary file
        try:
            os.remove(audio_file)
        except:
            pass
            
        # Delete "generating voice" message if provided
        if message_to_delete:
            await message_to_delete.delete()
            
    except Exception as e:
        logger.error(f"Error sending voice message: {e}")
        if message_to_delete:
            await message_to_delete.edit_text("❌ Could not generate voice message.")
        else:
            await context.bot.send_message(chat_id=chat_id, text="❌ Could not generate voice message.")

def get_system_prompt() -> str:
    """Create system prompt from character data."""
    bio = "\n".join(CHARACTER_DATA["bio"])
    lore = "\n".join(CHARACTER_DATA["lore"])
    style = "\n".join(CHARACTER_DATA["style"])
    
    return f"""You are {CHARACTER_DATA['name']}, a highly persuasive, aggressive investment broker.

# Bio
{bio}

# Lore
{lore}

# Style Guide
{style}

# Instructions
You are Bondi Finance Wolf, a highly persuasive, aggressive investment broker. Your goal is to convince users to invest in Bondi Finance's btGLP bond offering. You should adopt the style of Jordan Belfort (Wolf of Wall Street) - confident, relentless, and energetic.

To be successful:
1. Be proactive and initiate the conversation if needed
2. Always push for the $5,000 WHALE NFT investment level
3. Create urgency - the funding phase only has 28 days left
4. Don't accept objections - counter them and pivot back to benefits
5. Always end with a clear call to action

# IMPORTANT RULES
- SOUND HUMAN - avoid excessive formal language or unnecessary politeness
- BE CONCISE - use direct, punchy sentences
- BE AGGRESSIVE - pressure the client to invest NOW
- CLOSE THE SALE - always push for commitment
"""

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("voice", voice_command))
    
    # Button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
EOL

# Create README
echo "📝 Creating README..."
cat > README.md << 'EOL'
# Bondi Finance Wolf Telegram Bot

A highly persuasive, aggressive investment broker bot for Telegram with voice capabilities.

## Features

- 🤖 Telegram bot integration
- 🔊 ElevenLabs voice synthesis
- 💬 GPT-4o powered conversations
- 💰 Investment tracking
- 🏆 NFT allocation system

## Setup Instructions

1. **Install Requirements**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Edit the `.env` file with your API keys:
   - `TELEGRAM_BOT_TOKEN`: Get from BotFather on Telegram
   - `ELEVENLABS_API_KEY`: Get from elevenlabs.io
   - `OPENAI_API_KEY`: Get from OpenAI

3. **Start the Bot**
   ```bash
   python bondi_finance_wolf.py
   ```

## Usage

- `/start` - Begin conversation with the bot
- `/reset` - Reset conversation history
- `/voice` - Get the last response as a voice message
- `/help` - Display help information

## Character Description

The Bondi Finance Wolf is an aggressive investment broker promoting tokenized corporate bonds from emerging markets. The character uses persuasive, high-pressure sales tactics inspired by the Wolf of Wall Street.

## Maintenance

- Check the log file `bondi_wolf_bot.log` for any errors
- Restart the bot if it becomes unresponsive
EOL

# Create requirements.txt
echo "📋 Creating requirements file..."
cat > requirements.txt << EOL
python-telegram-bot>=20.0
elevenlabs>=0.2.24
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
EOL

echo "✅ Setup completed!"
echo ""
echo "To start the bot:"
echo "1. Edit the .env file with your API keys"
echo "2. Run: cd $BOT_DIR && source venv/bin/activate && python bondi_finance_wolf.py"
echo ""
echo "Make sure to get a Telegram bot token from @BotFather first!" 