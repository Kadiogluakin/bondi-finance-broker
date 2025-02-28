# Bondi Finance Wolf Telegram Client

This is a voice-enabled Telegram client that allows you to send text messages, voice messages, and make real phone calls as the Bondi Finance Wolf persona. The client integrates with ElevenLabs for voice generation and Twilio for making actual phone calls.

## Features

- **Telegram Integration**: Send text and voice messages through your Telegram account
- **ElevenLabs Voice Generation**: Generate realistic voice messages using ElevenLabs' advanced voice synthesis
- **Twilio Voice Calls**: Make actual phone calls with dynamic interactive scripts
- **Bondi Finance Wolf Persona**: Uses a character designed for investment pitching

## Setup

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Telegram API credentials
- ElevenLabs API key
- Twilio account and credentials
- Ngrok account (for Twilio webhooks)

### Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   cd telegram-bot
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating the following files:

   - `.env.telegram` for Telegram and ElevenLabs configuration
   - `.env.twilio` for Twilio configuration

4. Fill in your API credentials in the appropriate env files.

### Telegram Setup

1. Go to https://my.telegram.org/apps and create a new application
2. Fill in `.env.telegram` with your API_ID, API_HASH, and PHONE_NUMBER
3. Also add your ELEVENLABS_XI_API_KEY to this file

### Twilio Setup

1. Create a Twilio account at https://www.twilio.com/
2. Purchase a phone number to make calls from
3. Fill in `.env.twilio` with your TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER
4. Sign up for Ngrok at https://ngrok.com/ and get an auth token
5. Add your NGROK_AUTH_TOKEN to the `.env.twilio` file

## Setting up Ngrok for Twilio Webhooks

For Twilio to make calls and handle responses, you need a public URL that Twilio can reach. We use ngrok to create a secure tunnel to your local server.

### Quick Setup

We've created a helper script to set up ngrok for you:

```bash
# Make the script executable if needed
chmod +x setup_ngrok.py

# Run the setup script
python setup_ngrok.py
```

The script will:
1. Check if ngrok is installed
2. Guide you through getting an ngrok authtoken (if needed)
3. Update your `.env.twilio` file with the token
4. Test the connection

### Manual Setup

If you prefer to set up ngrok manually:

1. Sign up for a free account at [ngrok.com](https://ngrok.com/signup)
2. Get your authtoken from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Install ngrok on your system
4. Configure ngrok with your authtoken:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```
5. Update your `.env.twilio` file with your ngrok token.

## Usage

### Telegram Voice Client

Run the Telegram client with:

```
python telegram_voice_client_with_calls.py
```

The interactive menu provides the following options:

1. **Send message with voice attachment**: Send a text message with an accompanying voice message
2. **Send voice pitch sequence**: Send a series of voice messages following the Bondi Finance script
3. **Make a real voice call (via Twilio)**: Initiate a phone call to a specified number
4. **List recent contacts**: Display recent Telegram contacts
5. **Test voice generation**: Generate a voice clip without sending it
6. **Exit**: Quit the application

### Real Voice Calls with Twilio

Run the Twilio voice call server with:

```
python bondi_finance_voice_calls.py
```

This will:
1. Start a Flask server to handle Twilio webhooks
2. Set up an Ngrok tunnel to expose the server publicly
3. Provide an interactive menu for initiating calls

When a call is made:
1. The Bondi Finance Wolf intro script plays
2. The call follows an interactive script based on user responses
3. The conversation is dynamically adapted to objections or interest

## Troubleshooting

### Webhook URL Issues

If you see a warning about "No webhook URL available - run ngrok first", try:

1. Run the `setup_ngrok.py` script to set up ngrok properly
2. Make sure port 5001 is not in use by another application
3. Check the logs for errors related to ngrok authentication

### Port 5000 Already in Use

If you see an error about "Port 5000 is in use by another program" when running the voice call server:

1. We've updated the code to use port 5001 instead of 5000
2. If you still see this error, you can edit `bondi_finance_voice_calls.py` and change the port number in both the `start_server()` and `start_ngrok()` functions
3. On macOS, port 5000 is commonly used by AirPlay Receiver. You can disable it in System Preferences -> General -> AirDrop & Handoff

### Twilio Phone Number Not Working

If calls are not working:

1. Make sure your Twilio account is active and has available funds
2. Verify that the phone number in your `.env.twilio` file is correct
3. Ensure you've verified the destination phone number in your Twilio trial account
4. Check the Twilio console for any error messages

### Voice Generation Issues

If voice generation is not working:

1. Check that your ElevenLabs API key is correctly set in your `.env` file
2. Ensure you have credits available in your ElevenLabs account
3. Try the "Test voice generation" option in the interactive menu to verify your setup

## Security Notes

- Keep your API keys and credentials secure
- The `.env` files contain sensitive information and should never be committed to version control
- The client runs with your actual Telegram account, so use responsibly
- Twilio calls will be charged to your Twilio account based on their pricing

## License

This project is for demonstration purposes only and should be used responsibly and in accordance with all applicable laws and regulations, including telemarketing laws.
