#!/usr/bin/env python3
"""
Environment variable loader for the Bondi Finance telegram bot.
This script loads environment variables from the .env file and outputs
diagnostic information about which critical variables are present or missing.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Get the script directory
script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
project_root = script_dir.parent

# Path to the .env file (in the project root)
env_path = project_root / '.env'
twilio_env_path = script_dir / '.env.twilio'

# Print starting message
print(f"Loading environment variables from {env_path}")

# Load environment variables
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded variables from {env_path}")
else:
    print(f"❌ .env file not found at {env_path}")
    sys.exit(1)

# Also load Twilio-specific variables if they exist
if twilio_env_path.exists():
    load_dotenv(dotenv_path=twilio_env_path, override=True)
    print(f"✅ Loaded Twilio variables from {twilio_env_path}")

# Check for critical environment variables
critical_vars = [
    'ELEVENLABS_XI_API_KEY',  
    'ELEVENLABS_AGENT_ID',
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER'
]

# Check for nested formats too
nested_vars = {
    'ELEVENLABS_XI_API_KEY': 'CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_XI_API_KEY',
    'ELEVENLABS_VOICE_ID': 'CHARACTER.BONDI_FINANCE_BROKER.ELEVENLABS_VOICE_ID',
    'ELEVENLABS_AGENT_ID': None,  # No nested equivalent
}

missing_vars = []
for var in critical_vars:
    value = os.getenv(var)
    if not value and var in nested_vars and nested_vars[var]:
        # Try to get nested variant
        nested_value = os.getenv(nested_vars[var])
        if nested_value:
            # Copy the nested value to the standard variable
            os.environ[var] = nested_value
            print(f"ℹ️ Using {nested_vars[var]} for {var}")
            continue
    
    if not value:
        missing_vars.append(var)

if missing_vars:
    print("\n❌ Missing critical environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\nPlease ensure these variables are set in your .env file.")
else:
    print("\n✅ All critical environment variables are set")

# Additional checks for API URLs
ngrok_url = os.getenv('NGROK_URL')
if ngrok_url:
    print(f"✅ NGROK_URL is set to {ngrok_url}")
else:
    print("⚠️ NGROK_URL is not set - Twilio webhooks may not work correctly")

# Print detailed information about Twilio settings
if all([os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"), os.getenv("TWILIO_PHONE_NUMBER")]):
    print("\n📞 Twilio configuration:")
    print(f"  Account SID: {os.getenv('TWILIO_ACCOUNT_SID')[:8]}...{os.getenv('TWILIO_ACCOUNT_SID')[-4:]}")
    print(f"  Phone Number: {os.getenv('TWILIO_PHONE_NUMBER')}")
    
    if ngrok_url:
        print(f"  Webhook URL: {ngrok_url}/incoming-call")
    else:
        print("  ⚠️ No webhook URL available - run ngrok first")

# Print information about ElevenLabs settings
if os.getenv("ELEVENLABS_XI_API_KEY"):
    print("\n🔊 ElevenLabs configuration:")
    print(f"  API Key: {os.getenv('ELEVENLABS_XI_API_KEY')[:8]}...{os.getenv('ELEVENLABS_XI_API_KEY')[-4:]}")
    if os.getenv("ELEVENLABS_AGENT_ID"):
        print(f"  Agent ID: {os.getenv('ELEVENLABS_AGENT_ID')}")
    else:
        print("  ⚠️ No Agent ID set")
    if os.getenv("ELEVENLABS_VOICE_ID"):
        print(f"  Voice ID: {os.getenv('ELEVENLABS_VOICE_ID')}")
    else:
        print("  ⚠️ No Voice ID set") 