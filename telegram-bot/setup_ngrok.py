#!/usr/bin/env python3
"""
Ngrok Setup Helper for Bondi Finance Voice Calls

This script helps you set up ngrok for the Bondi Finance voice calling feature.
It will:
1. Check if ngrok is installed
2. Allow you to update your ngrok authtoken
3. Test the ngrok connection
4. Update the .env.twilio file with the new authtoken

Usage:
    python setup_ngrok.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv, set_key
import re

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def install_ngrok():
    """Provide instructions to install ngrok"""
    print("\n===== NGROK INSTALLATION =====")
    print("Ngrok is not installed. Please install it by following these steps:")
    print("\n1. Go to https://ngrok.com/download and download the appropriate version for your system")
    print("2. Extract the downloaded file")
    print("3. Move the ngrok executable to a directory in your PATH")
    print("\nAlternatively, you can install it using:")
    print("  • Mac (Homebrew): brew install ngrok/ngrok/ngrok")
    print("  • Windows (Chocolatey): choco install ngrok")
    print("\nAfter installing, please run this script again.")
    sys.exit(1)

def get_new_authtoken():
    """Get a new authtoken from the user"""
    print("\n===== NGROK AUTHTOKEN SETUP =====")
    print("To get an ngrok authtoken:")
    print("1. Sign up for a free account at https://ngrok.com/signup")
    print("2. Go to https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. Copy your authtoken")
    
    authtoken = input("\nEnter your ngrok authtoken: ").strip()
    if not authtoken:
        print("No authtoken provided. Exiting.")
        sys.exit(1)
    
    # Very basic validation: check if it looks like an ngrok token
    if not re.match(r'^[a-zA-Z0-9_]{30,}$', authtoken):
        print("\nWarning: The token you provided doesn't match the expected format.")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Exiting. Please try again with a valid token.")
            sys.exit(1)
    
    return authtoken

def update_env_file(authtoken):
    """Update the .env.twilio file with the new authtoken"""
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    env_file = script_dir / '.env.twilio'
    
    if not env_file.exists():
        print(f"Error: {env_file} does not exist.")
        return False
    
    # Load the current env file
    load_dotenv(dotenv_path=env_file)
    
    # Update the NGROK_AUTH_TOKEN
    os.environ["NGROK_AUTH_TOKEN"] = authtoken
    
    # Write the changes back to the file
    with open(env_file, 'r') as file:
        lines = file.readlines()
    
    with open(env_file, 'w') as file:
        token_updated = False
        for line in lines:
            if line.startswith('NGROK_AUTH_TOKEN='):
                file.write(f'NGROK_AUTH_TOKEN={authtoken}\n')
                token_updated = True
            else:
                file.write(line)
        
        if not token_updated:
            file.write(f'\nNGROK_AUTH_TOKEN={authtoken}\n')
    
    print(f"\nUpdated {env_file} with new authtoken.")
    return True

def test_ngrok_connection():
    """Test ngrok connection by starting a temporary tunnel"""
    print("\n===== TESTING NGROK CONNECTION =====")
    print("Starting a temporary ngrok tunnel to verify your authtoken...")
    
    try:
        # Configure ngrok with the authtoken
        subprocess.run(['ngrok', 'config', 'add-authtoken', os.environ.get('NGROK_AUTH_TOKEN')], 
                       capture_output=True, check=True)
        
        # Start a tunnel in the background
        process = subprocess.Popen(['ngrok', 'http', '5001', '--log=stdout'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("Ngrok tunnel started successfully!")
            print("Terminating test tunnel...")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"Error starting ngrok: {stderr}")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"Error configuring ngrok: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("\n=== BONDI FINANCE VOICE CALLS - NGROK SETUP ===\n")
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        install_ngrok()
    
    # Get authtoken
    authtoken = get_new_authtoken()
    
    # Update env file
    if not update_env_file(authtoken):
        print("Failed to update .env.twilio file.")
        sys.exit(1)
    
    # Test ngrok connection
    if test_ngrok_connection():
        print("\n✅ Ngrok setup complete!")
        print("\nYou can now run the Bondi Finance voice call server:")
        print("    python bondi_finance_voice_calls.py")
        print("\nThis will start the server on port 5001 and establish an ngrok tunnel.")
        print("The webhook URL for Twilio will be displayed in the server logs.")
    else:
        print("\n❌ Ngrok setup failed. Please check your authtoken and try again.")

if __name__ == "__main__":
    main() 