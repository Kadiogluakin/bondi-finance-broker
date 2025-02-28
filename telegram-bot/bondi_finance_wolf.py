#!/usr/bin/env python3
import os
import logging
import time
import json
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import openai
import io

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# ElevenLabs credentials from .env file
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "XPwgonYgvZVO8jPcWGpu")  # Wolf-like aggressive sales voice
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"  # Try a different model
ELEVENLABS_STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.6"))
ELEVENLABS_SIMILARITY_BOOST = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.8"))

# Configure API clients
openai.api_key = OPENAI_API_KEY

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

async def generate_voice_message(text):
    try:
        # Log the request to help with debugging
        logger.info(f"Generating voice for text: {text[:100]}...")
        
        # Voice generation settings following documentation
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": ELEVENLABS_MODEL_ID,
            "voice_settings": {
                "stability": ELEVENLABS_STABILITY,
                "similarity_boost": ELEVENLABS_SIMILARITY_BOOST
            }
        }
        
        # Log the full request for debugging
        logger.info(f"Request URL: {url}")
        logger.info(f"Request headers: {headers}")
        logger.info(f"Request data: {json.dumps(data)}")
        
        # Make the API request
        response = requests.post(url, json=data, headers=headers)
        
        # Log the response status and headers
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"Voice generation successful, received {len(response.content)} bytes of audio data")
            # Create BytesIO object for the audio content
            audio_data = io.BytesIO(response.content)
            # Ensure file pointer is at the beginning
            audio_data.seek(0)
            return audio_data
        else:
            # Log the error response
            error_text = response.text
            logger.error(f"Error response: {error_text}")
            return None
            
    except Exception as e:
        logger.error(f"Exception in voice generation: {str(e)}")
        return None

async def send_voice_message(update, context, text, message_to_delete=None):
    # Generate the voice message
    audio_data = await generate_voice_message(text)
    
    if audio_data:
        try:
            # Log before sending
            logger.info("Sending voice message to user...")
            
            # Use the BytesIO object directly
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=audio_data,
                caption="🐺 Bondi Finance Wolf 🐺"
            )
            logger.info("Voice message sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending voice message: {str(e)}")
            await update.message.reply_text(f"I couldn't send you a voice message, but here's my response: {text}")
            return False
    else:
        logger.error("No audio data was generated")
        await update.message.reply_text(f"I couldn't send you a voice message, but here's my response: {text}")
        return False

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
