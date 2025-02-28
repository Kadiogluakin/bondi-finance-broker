import os
import sys
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
def load_environment():
    # Load from parent directory first
    parent_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(parent_env_path):
        load_dotenv(parent_env_path)
        print(f"✅ Loaded variables from {parent_env_path}")
    
    # Load Twilio-specific variables from current directory
    twilio_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env.twilio')
    if os.path.exists(twilio_env_path):
        load_dotenv(twilio_env_path)
        print(f"✅ Loaded Twilio variables from {twilio_env_path}")

load_environment()

# Get ngrok URL from environment variables
ngrok_url_env = os.getenv('NGROK_URL')
print(f"\nNGROK_URL from environment: {ngrok_url_env}")

# Check if we can access the ngrok URL
def check_url(url, description):
    if not url:
        print(f"❌ {description} URL is not set")
        return False
    
    try:
        response = requests.head(url, timeout=5)
        print(f"✅ {description} URL ({url}) is accessible with status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ {description} URL ({url}) is not accessible: {str(e)}")
        return False

# Check if the Flask server is running locally
def check_flask_server():
    try:
        response = requests.head("http://localhost:5001", timeout=2)
        print(f"✅ Flask server is running locally with status code: {response.status_code}")
        
        # Check incoming-call endpoint
        try:
            response = requests.head("http://localhost:5001/incoming-call", timeout=2)
            print(f"✅ /incoming-call endpoint exists with status code: {response.status_code}")
        except Exception as e:
            print(f"❌ /incoming-call endpoint not accessible: {str(e)}")
            
        return True
    except Exception as e:
        print(f"❌ Flask server is not running locally: {str(e)}")
        return False

# Test TwiML response
def test_incoming_call_endpoint():
    try:
        # Create a minimal POST request that mimics Twilio's webhook
        data = {
            'CallSid': 'CA123456789',
            'From': '+16575323412',
            'To': '+16313492296'
        }
        response = requests.post("http://localhost:5001/incoming-call", data=data, timeout=5)
        print(f"✅ POST to /incoming-call endpoint successful with status code: {response.status_code}")
        print(f"Response content (first 100 chars): {response.text[:100]}...")
        return True
    except Exception as e:
        print(f"❌ POST to /incoming-call endpoint failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n=== BONDI FINANCE - CONNECTION CHECKER ===\n")
    
    print("\n--- NGrok Tunnel Check ---")
    check_url(ngrok_url_env, "NGrok (from environment)")
    
    if ngrok_url_env:
        # Check the /incoming-call endpoint via ngrok
        incoming_call_url = f"{ngrok_url_env}/incoming-call"
        check_url(incoming_call_url, "Ngrok /incoming-call endpoint")
    
    print("\n--- Flask Server Check ---")
    flask_running = check_flask_server()
    
    if flask_running:
        print("\n--- TwiML Response Test ---")
        test_incoming_call_endpoint()
    
    # Print instructions for fixing issues
    print("\n--- Recommendations ---")
    print("1. Make sure your Flask server is running with the command:")
    print("   python3 bondi_finance_voice_calls.py")
    print("2. When making a call, use the same ngrok URL that your Flask server is using:")
    print("   1. First check the URL in the Flask server logs")
    print("   2. Then set that URL in your environment: export NGROK_URL=https://your-ngrok-url.ngrok-free.app")
    print("   3. Then make the call using: python3 -c \"import bondi_finance_voice_calls; bondi_finance_voice_calls.make_call('+YOURNUMBER')\"") 