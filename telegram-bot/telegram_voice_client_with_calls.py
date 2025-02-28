#!/usr/bin/env python3
import os
import logging
import json
import asyncio
import io
import time
import requests
import tempfile
import sys
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PhoneNumberInvalid, PhoneCodeInvalid

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import our custom environment loader or fall back to direct dotenv loading
try:
    from load_env import critical_vars, missing_vars
    logger.info("Using custom environment loader")
except ImportError:
    logger.warning("Custom environment loader not found, falling back to dotenv")
    from dotenv import load_dotenv
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the .env file in the parent directory
    env_path = os.path.join(os.path.dirname(script_dir), '.env')
    
    print(f"Loading environment variables from {env_path}")
    load_dotenv(env_path)

# Check if Twilio is available
twilio_available = all(os.getenv(var) for var in ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER"])
if twilio_available:
    logger.info("Twilio credentials found. Call functionality is available.")
else:
    logger.warning("Twilio credentials not found. Call functionality will be limited.")

# Get ElevenLabs API key - try direct and character-specific formats
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_XI_API_KEY")
if not ELEVENLABS_API_KEY:
    ELEVENLABS_API_KEY = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_XI_API_KEY")
    if ELEVENLABS_API_KEY:
        logger.info("Using character-specific ElevenLabs API key")
    else:
        logger.warning("ElevenLabs API key not found. Voice functionality will be disabled.")

# Telegram client setup
API_ID = os.getenv("TELEGRAM_API_ID")
if not API_ID:
    API_ID = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.TELEGRAM_API_ID")

API_HASH = os.getenv("TELEGRAM_API_HASH")
if not API_HASH:
    API_HASH = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    logger.error("Telegram API credentials not found in environment variables.")
    logger.error("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH in your .env file.")
    sys.exit(1)

try:
    API_ID = int(API_ID)  # Convert to integer as required by pyrogram
except ValueError:
    logger.error(f"Invalid TELEGRAM_API_ID: {API_ID}. Must be an integer.")
    sys.exit(1)

# ElevenLabs configuration
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
if not ELEVENLABS_VOICE_ID:
    ELEVENLABS_VOICE_ID = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_VOICE_ID", "XPwgonYgvZVO8jPcWGpu")  # Default Wolf voice

ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_turbo_v2")
ELEVENLABS_STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.6"))
ELEVENLABS_SIMILARITY_BOOST = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.8"))
ELEVENLABS_STYLE = float(os.getenv("ELEVENLABS_STYLE", "0.0"))

PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER", "+541126629455")
TARGET_USERNAME = os.getenv("TELEGRAM_TARGET_USERNAME", "kadiogluakin")
TARGET_PHONE_NUMBER = os.getenv("TARGET_PHONE_NUMBER")  # Phone number to call via Twilio
SESSION_NAME = "bondi_wolf_session"  # Name for the Telegram session file

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

# Sample call scripts for voice messages and calls
CALL_SCRIPTS = [
    "Hey there! I've been watching your profile and I'm calling with an INCREDIBLE opportunity that's perfect for savvy investors like you. I'm talking about tokenized corporate bonds with real-world yields that make your savings account look like a joke.",
    
    "Listen, I don't offer this to just anyone. This Global Logistics Properties bond we're tokenizing? Normally requires a $200,000 minimum investment. But through Bondi Finance's revolutionary platform, you can get in for just $100. That's right, ONE HUNDRED DOLLARS to own part of a premium USD-denominated corporate bond.",
    
    "Now, the smart money - the investors who really understand opportunity - they're putting in $5,000 or more. Why? Because that gets you our exclusive WHALE NFT, which guarantees priority allocation in our upcoming token airdrop. The question is: are you smart money, or just another spectator watching others get wealthy?",
    
    "Our funding phase is already 15% filled and we've only got 28 days left. These opportunities don't sit around waiting. I've got five other calls to make after this to people who've been begging me for access. So what's it going to be? Are you in for $100, or are you ready to go big with $5,000 and join our whale club?"
]

# Sample messages to send
MESSAGES = [
    "Hey there! I've got an INCREDIBLE opportunity that's going to blow your mind. We're talking tokenized corporate bonds with yields that make your bank account look like a joke.",
    "Listen, I don't just show this to anyone. This GLP bond we're offering? Normally requires $200,000 minimum investment. But through Bondi Finance, you can get in for just $100. That's right, ONE HUNDRED DOLLARS.",
    "The smart money - people putting in $5,000 or more - they're getting our exclusive WHALE NFT. That guarantees them priority allocation in our token airdrop. The real question is: are you smart money or just another spectator?",
    "We've only got 28 days left in our funding phase and we're already 15% filled. You think this opportunity is going to sit around waiting for you? The clock is ticking!"
]

try:
    from bondi_finance_voice_calls import make_call as make_twilio_call
except ImportError:
    twilio_available = False
    print("Twilio voice call functionality not available. To enable it, install the required dependencies.")

async def generate_voice_message(text):
    """Generate voice message using ElevenLabs API"""
    try:
        # Check if API key is available
        if not ELEVENLABS_API_KEY:
            logger.error("ELEVENLABS_XI_API_KEY not found in environment variables. Voice generation will fail.")
            logger.info("Please set ELEVENLABS_XI_API_KEY in your .env file.")
            return None
            
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
        
        # Log the request details for debugging (excluding API key for security)
        logger.info(f"Request URL: {url}")
        logger.info(f"Request headers: {{'Accept': '{headers['Accept']}', 'Content-Type': '{headers['Content-Type']}'}}")
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

async def send_message_with_voice(client, target, message, voice_text=None):
    """
    Send a message with a voice attachment to a user
    
    Args:
        client: The Pyrogram client
        target: The target user ID or username
        message: The text message to send
        voice_text: The text to convert to voice (if None, uses the message)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logging.info(f"Generating voice for text: {voice_text[:100] if voice_text else message[:100]}...")
        
        if voice_text is None:
            voice_text = message
            
        voice_file = await generate_voice_message(voice_text)
        if voice_file is None:
            logging.error(f"Failed to generate voice for message to {target}")
            return False
        
        # Send the message
        await client.send_message(target, message)
        
        # Send the voice file directly without trying to read it again
        # voice_file is already a BytesIO object
        voice_file.name = "voice_message.mp3"  # Add a name attribute with appropriate extension
        
        # Send the voice file
        await client.send_voice(target, voice_file)
        logging.info(f"Successfully sent message with voice to {target}")
        return True
    except Exception as e:
        logging.error(f"Error sending message with voice to {target}: {str(e)}")
        return False

async def initiate_call(target_user, client):
    """Initiate a call to the target user."""
    try:
        logger.info(f"Attempting to call user: {getattr(target_user, 'first_name', 'Unknown')} (ID: {target_user.id})")
        
        # Send a text message first
        await client.send_message(
            target_user.id,
            "Bondi Finance Wolf here. I'm about to call you with an exclusive investment opportunity. Pick up!"
        )
        
        # In Pyrogram, we don't have direct access to phone numbers through the API
        # We'll need to use the phone number from the environment variables or user input
        import os  # Add the import here
        phone_number = os.getenv("TARGET_PHONE_NUMBER")
        
        if not phone_number:
            logger.warning("No target phone number configured. Falling back to voice messages.")
            # Send a text message instead of voice message if voice generation fails
            try:
                await send_message_with_voice(
                    client, target_user.id,
                    "I couldn't reach you by phone, so I'll send you some voice messages instead."
                )
            except Exception as e:
                logger.error(f"Error sending voice message: {str(e)}")
                await client.send_message(
                    target_user.id,
                    "I couldn't reach you by phone, so I'll send you some messages instead."
                )
            
            # Send each script as a text message if voice generation fails
            for script in CALL_SCRIPTS:
                try:
                    await send_message_with_voice(client, target_user.id, script)
                except Exception as e:
                    logger.error(f"Error sending voice message: {str(e)}")
                    await client.send_message(target_user.id, script)
                # Wait between messages
                await asyncio.sleep(1)
                
            logger.info("Completed sending voice message sequence")
            return False
            
        # If Twilio is available, attempt to make a call
        if twilio_available:
            try:
                # Import the function in this scope to avoid circular imports
                from bondi_finance_voice_calls import make_call
                
                # Make the call
                call_result = make_call(phone_number)
                
                if call_result:
                    logger.info(f"Successfully initiated call to {phone_number} with SID: {call_result}")
                    await client.send_message(
                        target_user.id,
                        "I'm calling you now! Pick up to hear about an exclusive investment opportunity with Bondi Finance!"
                    )
                    return True
                else:
                    logger.error("Call initiation failed. Falling back to voice messages.")
            except Exception as e:
                logger.error(f"Error making call via Twilio: {str(e)}")
                logger.error("Falling back to voice messages.")
        else:
            logger.warning("Twilio not configured. Falling back to voice messages.")
        
        # If we reached here, Twilio call failed or is not available
        # Fall back to sending voice messages
        try:
            await send_message_with_voice(
                client, target_user.id,
                "I tried to call you but couldn't get through. Let me tell you about this opportunity via voice messages."
            )
        except Exception as e:
            logger.error(f"Error sending voice message: {str(e)}")
            await client.send_message(
                target_user.id,
                "I tried to call you but couldn't get through. Let me tell you about this opportunity via messages."
            )
        
        # Send each script as a text message if voice generation fails
        for script in CALL_SCRIPTS:
            try:
                await send_message_with_voice(client, target_user.id, script)
            except Exception as e:
                logger.error(f"Error sending voice message: {str(e)}")
                await client.send_message(target_user.id, script)
            # Wait between messages
            await asyncio.sleep(1)
            
        logger.info("Completed sending voice message sequence (fallback)")
        return False
    except Exception as e:
        logger.error(f"Error in initiate_call: {str(e)}")
        return False

async def list_recent_contacts(client, limit=5):
    """List recent contacts from Telegram."""
    try:
        dialogs = await client.get_dialogs(limit=limit)
        print("\nRecent Contacts:")
        print("----------------")
        for i, dialog in enumerate(dialogs):
            if dialog.is_user:
                print(f"{i+1}. {dialog.name} ({dialog.entity.id})")
                if hasattr(dialog.entity, 'phone') and dialog.entity.phone:
                    print(f"   Phone: {dialog.entity.phone}")
        return True
    except Exception as e:
        logging.error(f"Error listing recent contacts: {str(e)}")
        return False

def check_twilio_and_ngrok_status():
    """Check if Twilio is properly configured and ngrok URL is set up."""
    if not twilio_available:
        return False, "Twilio is not configured. Please set up Twilio credentials in .env.twilio file."
    
    ngrok_url = os.getenv("NGROK_URL")
    if not ngrok_url:
        return False, "Ngrok URL is not set. Please run 'python3 setup_ngrok.py' first to set up ngrok."
    
    return True, "Twilio and ngrok are properly configured."

async def interactive_mode(client):
    """Interactive mode for the Telegram voice client."""
    import os  # Add the import here
    
    while True:
        print("\n=== Bondi Finance Wolf Telegram Client ===")
        print("1. Send message with voice attachment")
        print("2. Call user (voice call or message sequence)")
        print("3. List recent contacts")
        print("4. Test voice generation")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            phone = input("Enter phone number or username: ")
            message = input("Enter text message: ")
            voice_text = input("Enter voice message text (or press Enter to use the same as text message): ")
            
            if voice_text.strip() == "":
                voice_text = message
            
            result = await send_message_with_voice(client, phone, message, voice_text)
            if result:
                print("Message sent successfully!")
            else:
                print("Failed to send message.")
                
        elif choice == "2":
            phone_or_username = input("Enter phone number or username: ")
            try:
                # First try to resolve as a username
                user = None
                target_phone = None
                
                if phone_or_username.startswith("+") or phone_or_username.isdigit():
                    # This looks like a phone number, we'll use it for Twilio calling
                    logger.info(f"Using phone number for Twilio call: {phone_or_username}")
                    target_phone = phone_or_username
                    if not target_phone.startswith('+'):
                        target_phone = '+' + target_phone
                        
                    # If Twilio is available, make a direct call without trying to find the user in Telegram
                    twilio_ready, twilio_msg = check_twilio_and_ngrok_status()
                    if twilio_ready:
                        try:
                            # Import the function in this scope to avoid circular imports
                            from bondi_finance_voice_calls import make_call
                            
                            # Set the target phone number in environment for the call function
                            os.environ["TARGET_PHONE_NUMBER"] = target_phone
                            logger.info(f"Set TARGET_PHONE_NUMBER to {target_phone} for Twilio call")
                            
                            # Make the call
                            call_result = make_call(target_phone)
                            
                            if call_result:
                                logger.info(f"Successfully initiated call to {target_phone} with SID: {call_result}")
                                print(f"Call initiated to {target_phone}! The Bondi Finance Wolf is now pitching to the contact.")
                            else:
                                logger.error("Call initiation failed.")
                                print("Failed to initiate call. Please check logs for details.")
                        except Exception as e:
                            logger.error(f"Error making call via Twilio: {str(e)}")
                            print(f"Error making call: {str(e)}")
                    else:
                        logger.warning(f"Cannot make direct phone calls: {twilio_msg}")
                        print(f"Cannot make direct phone calls: {twilio_msg}")
                        print("Try running 'python3 setup_ngrok.py' to set up ngrok and then try again.")
                else:
                    # This is a username, try to resolve it in Telegram
                    logger.info(f"Resolving username: {phone_or_username}")
                    try:
                        user = await client.get_users(phone_or_username)
                        logger.info(f"Found user: {getattr(user, 'first_name', 'Unknown')}")
                        
                        # If we need to call this user, we need their phone number
                        if twilio_available:
                            target_phone = input("Enter phone number for Twilio call (with country code): ")
                            if target_phone and not target_phone.startswith('+'):
                                target_phone = '+' + target_phone
                            
                            # Set the target phone number in environment for the call function
                            if target_phone:
                                os.environ["TARGET_PHONE_NUMBER"] = target_phone
                                logger.info(f"Set TARGET_PHONE_NUMBER to {target_phone} for Twilio call")
                        
                        # Proceed with the call or message sequence
                        result = await initiate_call(user, client)
                        if result:
                            if twilio_available and target_phone:
                                print(f"Call initiated to {target_phone}! The Bondi Finance Wolf is now pitching to the contact.")
                            else:
                                print("Voice pitch sequence sent successfully!")
                        else:
                            print("Failed to initiate call or send voice messages.")
                    except Exception as e:
                        logger.error(f"Error resolving username: {str(e)}")
                        print(f"Could not find user with username '{phone_or_username}'. Error: {str(e)}")
                
            except Exception as e:
                logger.error(f"Error in call option: {str(e)}")
                print(f"Error: {str(e)}")
                
        elif choice == "3":
            limit = int(input("Enter number of contacts to list: ") or "5")
            await list_recent_contacts(client, limit)
                
        elif choice == "4":
            text = input("Enter text to convert to voice: ")
            if text:
                print("Generating voice message...")
                voice_file = await generate_voice_message(text)
                if voice_file:
                    print(f"Voice message generated successfully: {voice_file}")
                    # Play the voice message if possible
                    try:
                        import os
                        os.system(f"ffplay -nodisp -autoexit {voice_file} 2>/dev/null")
                        print("Voice message played.")
                    except Exception as e:
                        print(f"Could not play voice message: {e}")
                else:
                    print("Failed to generate voice message.")
            else:
                print("No text provided.")
                
        elif choice == "5":
            print("Exiting...")
            return False
                
        else:
            print("Invalid choice. Please try again.")
    
    return True

async def main():
    """Main function to run the script."""
    # Initialize Telegram client
    client = Client(SESSION_NAME, API_ID, API_HASH, phone_number=PHONE_NUMBER)
    await client.start()
    
    print("Connected to Telegram!")
    
    # Enter interactive mode
    keep_running = True
    while keep_running:
        keep_running = await interactive_mode(client)
    
    # Disconnect when done
    try:
        await client.disconnect()
        print("Disconnected from Telegram.")
    except Exception as e:
        logger.error(f"Error disconnecting client: {str(e)}")
        print("Error disconnecting. Client may already be disconnected or in use.")
        # Force stop all network tasks
        if hasattr(client, 'session'):
            try:
                await client.session.stop()
                print("Forced session to stop.")
            except Exception as session_error:
                logger.error(f"Error stopping session: {str(session_error)}")
                
    print("Application closed.")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 