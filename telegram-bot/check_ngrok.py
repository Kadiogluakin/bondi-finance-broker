#!/usr/bin/env python3
"""
Check for active ngrok tunnels and display their URLs.
"""

import sys
import os
import logging
from pyngrok import ngrok

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def check_tunnels():
    """Check for active ngrok tunnels"""
    try:
        tunnels = ngrok.get_tunnels()
        
        if not tunnels:
            logger.info("No active ngrok tunnels found.")
            logger.info("Please run 'python bondi_finance_voice_calls.py' to start a tunnel.")
            return None
        
        logger.info(f"Found {len(tunnels)} active ngrok tunnel(s):")
        
        for i, tunnel in enumerate(tunnels):
            logger.info(f"  {i+1}. {tunnel.public_url} -> {tunnel.config['addr']}")
            
            # If this is a tunnel for port 5001, set it as the NGROK_URL
            if tunnel.config['addr'].endswith(':5001') and tunnel.proto == 'https':
                os.environ["NGROK_URL"] = tunnel.public_url
                logger.info(f"✅ Setting NGROK_URL to {tunnel.public_url}")
                logger.info(f"   This URL can be used for Twilio webhooks.")
                
        return tunnels
    
    except Exception as e:
        logger.error(f"Error checking ngrok tunnels: {str(e)}")
        return None

def main():
    """Main function"""
    print("\n=== BONDI FINANCE - NGROK TUNNEL CHECKER ===\n")
    
    # Check if pyngrok is installed
    try:
        import pyngrok
    except ImportError:
        logger.error("pyngrok is not installed. Please run: pip install pyngrok")
        sys.exit(1)
    
    # Check tunnels
    tunnels = check_tunnels()
    
    if tunnels:
        print("\nTo use one of these URLs for Twilio calls:")
        print("1. Edit your .env.twilio file and add:")
        print(f"   NGROK_URL={tunnels[0].public_url}")
        print("2. Or just restart the bondi_finance_voice_calls.py script")
    else:
        print("\nNo active tunnels found. To create a tunnel:")
        print("1. Run the setup_ngrok.py script to set up ngrok")
        print("2. Then run bondi_finance_voice_calls.py to create a tunnel")

if __name__ == "__main__":
    main() 