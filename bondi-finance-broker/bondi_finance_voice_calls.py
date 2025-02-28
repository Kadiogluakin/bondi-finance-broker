#!/usr/bin/env python3
"""
Bondi Finance Voice Call Server - Handles Twilio voice calls using ElevenLabs for
voice generation and conversational agents.
"""

import os
import sys
import tempfile
import logging
import json
import asyncio
import requests
import time
import subprocess
from datetime import datetime
from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import threading
from pyngrok import ngrok
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('voice_calls.log')
    ]
)
logger = logging.getLogger(__name__)

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

# Try to import our custom environment loader or fall back to direct dotenv loading
try:
    # Import the custom loader which will load both .env and .env.twilio
    from load_env import critical_vars, missing_vars
    logger.info("Using custom environment loader")
except ImportError:
    logger.warning("Custom environment loader not found, falling back to dotenv")
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the .env file in the parent directory
    env_path = os.path.join(os.path.dirname(script_dir), '.env')
    # Path to the .env.twilio file in the current directory
    twilio_env_path = os.path.join(script_dir, '.env.twilio')
    
    # Load both env files
    load_dotenv(env_path)
    logger.info(f"Loaded environment variables from {env_path}")
    
    if os.path.exists(twilio_env_path):
        load_dotenv(twilio_env_path, override=True)
        logger.info(f"Loaded Twilio variables from {twilio_env_path}")

# ElevenLabs configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_XI_API_KEY")
if not ELEVENLABS_API_KEY:
    ELEVENLABS_API_KEY = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_XI_API_KEY")
    if ELEVENLABS_API_KEY:
        logger.info("Using character-specific ElevenLabs API key")
    else:
        logger.error("ElevenLabs API key not found. Voice generation will not work.")

ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
if not ELEVENLABS_AGENT_ID:
    logger.warning("ELEVENLABS_AGENT_ID not found. Conversational Agent will not work.")

ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
if not ELEVENLABS_VOICE_ID:
    ELEVENLABS_VOICE_ID = os.getenv("CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_VOICE_ID", "XPwgonYgvZVO8jPcWGpu")  # Default Wolf voice

# Twilio configuration
# Make sure to reload these values in case they were updated after loading .env.twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Make sure we're using the correct Twilio phone number
if TWILIO_PHONE_NUMBER:
    logger.info(f"Using Twilio phone number: {TWILIO_PHONE_NUMBER}")
else:
    logger.error("TWILIO_PHONE_NUMBER not found in environment variables. Voice calls will not work.")

# Get the ngrok URL if available
NGROK_URL = os.getenv("NGROK_URL")
if NGROK_URL:
    logger.info(f"Using ngrok URL for Twilio webhooks: {NGROK_URL}")
else:
    logger.warning("NGROK_URL not found. Twilio webhooks may not work correctly.")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
    logger.error("Twilio credentials not found in environment variables. Voice calls will not work.")
    logger.info("Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in your .env file.")

app = Flask(__name__)

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("Twilio client initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Twilio client: {str(e)}")
else:
    logger.warning("Twilio credentials not found. Call functionality will be limited.")

# Track active calls
active_calls = {}

def connect_to_elevenlabs_agent(user_input, call_sid=None, is_first_message=False):
    """Connect to ElevenLabs conversational agent and get response"""
    try:
        if not ELEVENLABS_API_KEY:
            logger.error("ElevenLabs API key not found. Cannot connect to agent.")
            return "I'm sorry, but I'm having trouble connecting to my system. Please try again later."
            
        if not ELEVENLABS_AGENT_ID:
            logger.error("ElevenLabs Agent ID not found. Cannot connect to conversational agent.")
            return "I'm sorry, but I'm having trouble accessing my knowledge base. Please try again later."
        
        # Prepare the message for the agent
        history = []
        if call_sid and call_sid in active_calls and 'conversation' in active_calls[call_sid]:
            history = active_calls[call_sid]['conversation']
        
        # Define initial message if this is the first interaction
        if is_first_message:
            # Add context from character data to help the agent understand its role
            system_message = "You are the Bondi Finance Wolf, an aggressive investment broker. "
            system_message += "You specialize in tokenized corporate bonds, specifically the Global Logistics Properties bond. "
            system_message += "Your goal is to convince the caller to invest, with a minimum of $100, but preferably $5,000 to get the WHALE NFT. "
            system_message += "Be persuasive, create urgency, and counter objections forcefully. Always push for the investment."
            
            # Updated API endpoint for creating a new conversation
            url = f"https://api.elevenlabs.io/v1/conversation"
            
            data = {
                "agent_id": ELEVENLABS_AGENT_ID,
                "audio_settings": {
                    "output_format": "mulaw_8000",
                    "stability": 0.6,
                    "similarity_boost": 0.8,
                    "style": 0.7,
                    "use_speaker_boost": True
                },
                "system_message": system_message,
                "character": {
                    "name": CHARACTER_DATA["name"],
                    "bio": "\n".join(CHARACTER_DATA["bio"]),
                    "lore": "\n".join(CHARACTER_DATA["lore"]),
                    "style": "\n".join(CHARACTER_DATA["style"]),
                },
                "messages": [{
                    "role": "user",
                    "content": user_input or "Hello"
                }]
            }
        else:
            # For ongoing conversation, use the conversation ID
            conversation_id = active_calls[call_sid].get('conversation_id')
            if not conversation_id:
                logger.error(f"No conversation ID found for call {call_sid}")
                return "I apologize, but I seem to have lost track of our conversation. Let me restart. What can I help you with regarding our investment opportunities?"
                
            # Updated API endpoint for continuing an existing conversation
            url = f"https://api.elevenlabs.io/v1/conversation/{conversation_id}/message"
            
            data = {
                "message": {
                    "role": "user",
                    "content": user_input
                }
            }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        logger.info(f"Sending request to ElevenLabs Conversation API: {url}")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            logger.error(f"Error connecting to ElevenLabs Conversation API: {response.status_code} - {response.text}")
            return "I'm having trouble processing your request. Let me try a different approach. Our Global Logistics Properties bond offers an exceptional investment opportunity with just a $100 minimum. Are you interested in learning more?"
        
        response_data = response.json()
        
        # Store conversation ID for future interactions
        if call_sid and is_first_message and 'conversation_id' in response_data:
            if call_sid not in active_calls:
                active_calls[call_sid] = {}
            active_calls[call_sid]['conversation_id'] = response_data['conversation_id']
            
            # Store conversation history
            if 'conversation' not in active_calls[call_sid]:
                active_calls[call_sid]['conversation'] = []
                
            # Add user message to history
            active_calls[call_sid]['conversation'].append({
                "role": "user",
                "content": user_input or "Hello"
            })
            
            # Add agent response to history
            if 'response' in response_data:
                active_calls[call_sid]['conversation'].append({
                    "role": "assistant",
                    "content": response_data['response']['text']
                })
        
        # Get the agent's response text and audio
        if 'response' in response_data:
            return response_data['response']['text']
        else:
            logger.error("No response content found in API response")
            return "I'm sorry, I'm having trouble formulating my thoughts. Let me tell you about our incredible investment opportunity with tokenized corporate bonds instead."
            
    except Exception as e:
        logger.error(f"Error connecting to ElevenLabs Conversation API: {str(e)}")
        return "I apologize for the technical difficulties. Let me tell you directly - we're offering a Global Logistics Properties bond with just $100 minimum investment, normally requiring $200,000. Are you interested in this exclusive opportunity?"

@app.route('/incoming-call', methods=['POST'])
def incoming_call():
    """Handle incoming Twilio call"""
    try:
        # Get the caller's phone number
        caller = request.values.get('From', '')
        call_sid = request.values.get('CallSid', '')
        
        logger.info(f"Incoming call from {caller} with SID: {call_sid}")
        
        # Record call in active_calls
        active_calls[call_sid] = {
            'caller': caller,
            'start_time': time.time()
        }
        
        # Create a response
        response = VoiceResponse()
        
        # Get initial greeting from ElevenLabs Agent
        logger.info(f"Generating initial greeting for call {call_sid}")
        greeting = connect_to_elevenlabs_agent(None, call_sid, is_first_message=True)
        logger.info(f"Generated greeting: {greeting[:50]}...")
        
        # Add the Bondi Finance Wolf intro
        response.say(greeting, voice='man')
        
        # Pause for effect
        response.pause(length=1)
        
        # Gather any input
        gather = Gather(action='/agent-response', method='POST', input='speech dtmf', timeout=5, speechTimeout='auto')
        response.append(gather)
        
        # If no input, continue with the agent
        response.redirect('/agent-continue')
        
        logger.info(f"Successfully generated TwiML response for call {call_sid}")
        return str(response)
    except Exception as e:
        logger.error(f"Error in incoming-call route: {str(e)}", exc_info=True)
        # Return a simple response to avoid complete failure
        error_response = VoiceResponse()
        error_response.say("I apologize, but we're experiencing technical difficulties. Please try again later.", voice='man')
        return str(error_response)

@app.route('/agent-response', methods=['POST'])
def agent_response():
    """Handle user input and get agent response"""
    try:
        # Get the caller's input
        digits = request.values.get('Digits', '')
        speech = request.values.get('SpeechResult', '')
        call_sid = request.values.get('CallSid', '')
        
        logger.info(f"Agent response for call {call_sid}: Digits={digits}, Speech={speech}")
        
        # Use speech if available, otherwise digits
        user_input = speech if speech else digits
        
        # Create a response
        response = VoiceResponse()
        
        # If no input was detected, use a default question
        if not user_input:
            user_input = "Tell me more about this investment"
        
        logger.info(f"User input: {user_input}")
        
        # Get response from ElevenLabs Agent
        logger.info(f"Getting agent response for call {call_sid} with input: {user_input[:50]}...")
        agent_response_text = connect_to_elevenlabs_agent(user_input, call_sid)
        logger.info(f"Generated agent response: {agent_response_text[:50]}...")
        
        # Say the agent's response
        response.say(agent_response_text, voice='man')
        
        # Pause for effect
        response.pause(length=1)
        
        # Gather again for continued conversation
        gather = Gather(action='/agent-response', method='POST', input='speech dtmf', timeout=5, speechTimeout='auto')
        response.append(gather)
        
        # If no input, continue
        response.redirect('/agent-continue')
        
        logger.info(f"Successfully generated agent response TwiML for call {call_sid}")
        return str(response)
    except Exception as e:
        logger.error(f"Error in agent-response route: {str(e)}", exc_info=True)
        # Return a simple response to avoid complete failure
        error_response = VoiceResponse()
        error_response.say("I apologize, but we're experiencing technical difficulties. Please try again later.", voice='man')
        return str(error_response)

@app.route('/agent-continue', methods=['POST'])
def agent_continue():
    """Continue the conversation if there was no input"""
    try:
        call_sid = request.values.get('CallSid', '')
        
        logger.info(f"Agent continue for call {call_sid} due to no input")
        
        # Create a response
        response = VoiceResponse()
        
        # Get continuation from ElevenLabs Agent
        logger.info(f"Getting agent continuation for call {call_sid}")
        continuation = connect_to_elevenlabs_agent("The caller is silent. Ask them a direct question to encourage response.", call_sid)
        logger.info(f"Generated agent continuation: {continuation[:50]}...")
        
        # Say the continuation
        response.say(continuation, voice='man')
        
        # Gather again
        gather = Gather(action='/agent-response', method='POST', input='speech dtmf', timeout=5, speechTimeout='auto')
        response.append(gather)
        
        # If still no input, end call
        response.say("I appreciate your time today. If you change your mind about this incredible investment opportunity, please call back. This is the Bondi Finance Wolf, signing off.", voice='man')
        
        logger.info(f"Successfully generated agent continuation TwiML for call {call_sid}")
        return str(response)
    except Exception as e:
        logger.error(f"Error in agent-continue route: {str(e)}", exc_info=True)
        # Return a simple response to avoid complete failure
        error_response = VoiceResponse()
        error_response.say("I apologize, but we're experiencing technical difficulties. Please try again later.", voice='man')
        return str(error_response)

def make_call(phone_number):
    """Initiate a call to a phone number"""
    if not twilio_client:
        logger.error("Twilio client not initialized. Cannot make call.")
        return False
    
    try:
        # Format the phone number (ensure it has the +country code format)
        if not phone_number.startswith('+'):
            # Default to US format if no country code
            phone_number = '+1' + phone_number
            logger.info(f"Added default country code to phone number: {phone_number}")
        
        # Get the public URL for our webhook
        ngrok_url = os.getenv("NGROK_URL", "")
        
        # Check if ngrok_url is available and properly formatted
        if not ngrok_url:
            logger.warning("NGROK_URL environment variable not set. Webhook may not work.")
            # Try to get ngrok URL from ngrok API if tunnel is running
            try:
                # Get active tunnels using pyngrok
                from pyngrok import ngrok as pyngrok
                tunnels = pyngrok.get_tunnels()
                for tunnel in tunnels:
                    if tunnel.proto == "https":
                        ngrok_url = tunnel.public_url
                        logger.info(f"Found active ngrok tunnel: {ngrok_url}")
                        break
            except ImportError:
                logger.warning("pyngrok not installed. Cannot get ngrok tunnels.")
            except Exception as e:
                logger.error(f"Error getting ngrok tunnels: {str(e)}")
        
        # Build the webhook URL
        if ngrok_url:
            # Make sure it has https://
            if not ngrok_url.startswith('http'):
                ngrok_url = 'https://' + ngrok_url
            
            # Remove trailing slash if present
            if ngrok_url.endswith('/'):
                ngrok_url = ngrok_url[:-1]
                
            webhook_url = f"{ngrok_url}/incoming-call"
        else:
            # Use a default URL - this won't work in production
            webhook_url = "http://demo.twilio.com/docs/voice.xml"
            logger.warning(f"Using fallback webhook URL: {webhook_url} - this is only for testing")
        
        logger.info(f"Making Twilio call to {phone_number} using webhook URL: {webhook_url}")
        
        # Make the call
        call = twilio_client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url=webhook_url
        )
        
        logger.info(f"Call initiated to {phone_number} with SID: {call.sid}")
        return call.sid
        
    except Exception as e:
        logger.error(f"Error making call to {phone_number}: {str(e)}")
        return False

def start_server():
    """Start Flask server with ngrok tunnel"""
    # Start ngrok tunnel
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.daemon = True
    ngrok_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5001)

def start_ngrok():
    """Start ngrok tunnel to expose local server"""
    try:
        # Use existing ngrok URL from environment if available
        existing_ngrok_url = os.getenv("NGROK_URL")
        if existing_ngrok_url:
            logger.info(f"Using existing ngrok URL from environment: {existing_ngrok_url}")
            return
            
        # Connect to ngrok only if no URL is already set
        ngrok_auth = os.getenv("NGROK_AUTH_TOKEN")
        if ngrok_auth:
            ngrok.set_auth_token(ngrok_auth)
        
        # Open an HTTP tunnel on the specified port
        http_tunnel = ngrok.connect(5001)
        public_url = http_tunnel.public_url
        logger.info(f"Ngrok tunnel established at: {public_url}")
        
        # Store the ngrok URL in environment variable
        os.environ["NGROK_URL"] = public_url
        logger.info(f"Set NGROK_URL environment variable to: {public_url}")
        
    except Exception as e:
        logger.error(f"Error starting ngrok: {str(e)}")
        # If there's an error and we have an existing URL, just use that
        if os.getenv("NGROK_URL"):
            logger.info(f"Using existing NGROK_URL despite ngrok error: {os.getenv('NGROK_URL')}")

def interactive_mode():
    """Interactive mode for making calls"""
    print("\n=== Bondi Finance Wolf Voice Caller ===")
    print("1. Make a call")
    print("2. Exit")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == "1":
        phone_number = input("Enter phone number to call (with country code): ")
        if phone_number:
            call_sid = make_call(phone_number)
            if call_sid:
                print(f"Call initiated with SID: {call_sid}")
                print("The Bondi Finance Wolf is now pitching on the call...")
                print("Press Ctrl+C to exit when ready")
            else:
                print("Failed to initiate call.")
    
    elif choice == "2":
        return False
    
    return True

def main():
    """Main function"""
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give server time to start
    print("Starting server and ngrok tunnel...")
    time.sleep(5)
    
    # Enter interactive mode
    keep_running = True
    while keep_running:
        try:
            keep_running = interactive_mode()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            keep_running = input("Continue? (y/n): ").lower() == 'y'
    
    print("Bondi Finance Wolf Voice Caller terminated.")

if __name__ == "__main__":
    main() 