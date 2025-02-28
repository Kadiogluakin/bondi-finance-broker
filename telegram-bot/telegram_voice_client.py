#!/usr/bin/env python3
import os
import logging
import json
import asyncio
import io
import time
import requests
from telethon import TelegramClient, events
from telethon.tl import types
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Telegram client credentials
API_ID = int(os.getenv("TELEGRAM_API_ID", "23354561"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "b249dedc3254e65a0f90be0822d36b04")
PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER", "+541126629455")
TARGET_USERNAME = os.getenv("TELEGRAM_TARGET_USERNAME", "kadiogluakin")

# ElevenLabs configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_XI_API_KEY", "sk_f51ecfbd39832df5724b7025bc76a7a7ead7692ed65198d2")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "XPwgonYgvZVO8jPcWGpu")  # Wolf-like aggressive sales voice
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")  # Default model
ELEVENLABS_STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.6"))
ELEVENLABS_SIMILARITY_BOOST = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.8"))

# Character data for the Bondi Finance Wolf persona
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
        "Always push for higher investment amounts to qualify for the WHALE NFT."
    ]
}

# Sample messages to send
MESSAGES = [
    "Hey there! I've got an INCREDIBLE opportunity that's going to blow your mind. We're talking tokenized corporate bonds with yields that make your bank account look like a joke.",
    "Listen, I don't just show this to anyone. This GLP bond we're offering? Normally requires $200,000 minimum investment. But through Bondi Finance, you can get in for just $100. That's right, ONE HUNDRED DOLLARS.",
    "The smart money - people putting in $5,000 or more - they're getting our exclusive WHALE NFT. That guarantees them priority allocation in our token airdrop. The real question is: are you smart money or just another spectator?",
    "We've only got 28 days left in our funding phase and we're already 15% filled. You think this opportunity is going to sit around waiting for you? The clock is ticking!"
]

async def generate_voice_message(text):
    """Generate voice message using ElevenLabs API"""
    try:
        # Log the request to help with debugging
        logger.info(f"Generating voice for text: {text[:100]}...")
        
        # Voice generation settings
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

async def send_message_with_voice(client, target, message):
    """Send a text message followed by a voice message to a target user"""
    try:
        # Find the target user
        target_entity = await client.get_entity(target)
        
        # Send text message
        logger.info(f"Sending text message to {target}: {message[:50]}...")
        await client.send_message(target_entity, message)
        logger.info("Text message sent successfully")
        
        # Generate voice message
        audio_data = await generate_voice_message(message)
        
        if audio_data:
            # Send voice message
            logger.info(f"Sending voice message to {target}")
            await client.send_file(
                target_entity,
                audio_data,
                voice_note=True,  # This makes it appear as a voice message
                caption="🐺 Bondi Finance Wolf 🐺"
            )
            logger.info("Voice message sent successfully")
        else:
            logger.error("Failed to generate voice message, skipping")
    
    except Exception as e:
        logger.error(f"Error sending message to {target}: {str(e)}")

async def main():
    """Main function to set up and run the Telegram client"""
    # Start the client
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    
    # Log in info
    me = await client.get_me()
    logger.info(f"Successfully logged in as {me.first_name} (ID: {me.id})")
    
    # Send messages to the target user
    for message in MESSAGES:
        await send_message_with_voice(client, TARGET_USERNAME, message)
        # Wait between messages to avoid flood restrictions
        await asyncio.sleep(5)
    
    # Message handler for interactive mode
    @client.on(events.NewMessage)
    async def handler(event):
        # Log received message
        logger.info(f"Received message: {event.message.text}")
        
        # Generate a response based on the Wolf persona
        # In a real implementation, you might use an LLM like GPT here
        response = "Hey! You're talking to the Bondi Finance Wolf. I'm all about helping you make money with our exclusive bond offerings. How much are you looking to invest today? $100 for our OG NFT or $5,000 for the WHALE NFT?"
        
        # Send the response
        await send_message_with_voice(client, event.sender_id, response)
    
    logger.info("Telegram client set up complete. Listening for messages...")
    
    # Keep the client running
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 