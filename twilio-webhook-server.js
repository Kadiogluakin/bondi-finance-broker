import express from 'express';
import twilio from 'twilio';

// Create Express server
const app = express();
const PORT = process.env.TWILIO_WEBHOOK_PORT || 3456;

// Parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Enhanced logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  console.log('Headers:', JSON.stringify(req.headers, null, 2));
  console.log('Body:', JSON.stringify(req.body, null, 2));
  
  // Keep track of the original send method
  const originalSend = res.send;
  
  // Override the send method to log the response
  res.send = function(body) {
    console.log(`Response: ${body}`);
    return originalSend.call(this, body);
  };
  
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  console.log('Health check endpoint called');
  res.status(200).send('Server is healthy');
});

// TwiML endpoint - This handles the initial call
app.post('/twiml', (req, res) => {
  try {
    console.log('TwiML endpoint called with params:', req.body, req.query);
    
    // Get parameters from query string
    const callId = req.query.callId || '';
    const agentName = req.query.agentName || 'Jordan';
    const userPhone = req.query.userPhone || '';
    
    console.log(`Processing call: ID=${callId}, Agent=${agentName}, User=${userPhone}`);
    
    // Create a TwiML response
    const twiml = new twilio.twiml.VoiceResponse();
    
    // Add a greeting and gather user input
    twiml.say({ voice: 'man', language: 'en-US' }, 
      `Hello, this is ${agentName} from Bondi Finance. I'm calling about an incredible investment opportunity with our tokenized bonds. They offer exceptional stability with great returns.`);
    
    // Gather the caller's speech input
    twiml.gather({
      input: 'speech',
      action: '/gather',
      method: 'POST',
      speechTimeout: 'auto',
      language: 'en-US'
    }).say({ voice: 'man', language: 'en-US' }, 
      'Are you interested in hearing more about how you can earn stable yields while also securing our exclusive Whale NFT?');
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('TwiML response sent:', twiml.toString());
  } catch (error) {
    console.error('Error in /twiml endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      const errorTwiml = new twilio.twiml.VoiceResponse();
      errorTwiml.say('We encountered an error processing your call. Please try again later.');
      
      res.type('text/xml');
      res.status(200).send(errorTwiml.toString());
    } catch (innerError) {
      console.error('Failed to create error TwiML:', innerError);
      // Fallback to simple string response
      res.type('text/xml');
      res.status(200).send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>We encountered an error.</Say></Response>');
    }
  }
});

// Gather endpoint - This handles user's speech input
app.post('/gather', (req, res) => {
  try {
    console.log('Gather endpoint called with params:', req.body);
    
    // Get the user's speech input
    const userSpeech = req.body.SpeechResult || '';
    console.log('User speech:', userSpeech);
    
    // Create a TwiML response
    const twiml = new twilio.twiml.VoiceResponse();
    
    // Generate a response based on user input
    const responseText = generateSimpleResponse(userSpeech);
    
    // Add the response to TwiML
    twiml.say({ voice: 'man', language: 'en-US' }, responseText);
    
    // Add another gather to continue the conversation
    twiml.gather({
      input: 'speech',
      action: '/gather',
      method: 'POST',
      speechTimeout: 'auto',
      language: 'en-US'
    }).say({ voice: 'man', language: 'en-US' }, 'What are your thoughts about this investment opportunity?');
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('Gather response sent:', twiml.toString());
  } catch (error) {
    console.error('Error in /gather endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      const errorTwiml = new twilio.twiml.VoiceResponse();
      errorTwiml.say('We encountered an error processing your response. Please try again later.');
      
      res.type('text/xml');
      res.status(200).send(errorTwiml.toString());
    } catch (innerError) {
      console.error('Failed to create error TwiML:', innerError);
      // Fallback to simple string response
      res.type('text/xml');
      res.status(200).send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>We encountered an error.</Say></Response>');
    }
  }
});

// Status callback endpoint
app.post('/status', (req, res) => {
  try {
    console.log('Status callback received:', req.body);
    // Just acknowledge receipt of status update
    res.status(200).send('OK');
  } catch (error) {
    console.error('Error in /status endpoint:', error);
    res.status(200).send('Error handled');
  }
});

// Fallback route for any unhandled requests
app.use('*', (req, res) => {
  console.log(`Unhandled request: ${req.method} ${req.originalUrl}`);
  
  // If it's a Twilio request, return valid TwiML
  if (req.headers['user-agent'] && req.headers['user-agent'].includes('TwilioProxy')) {
    try {
      const twiml = new twilio.twiml.VoiceResponse();
      twiml.say('This endpoint is not configured. Please check your Twilio settings.');
      
      res.type('text/xml');
      res.status(200).send(twiml.toString());
    } catch (error) {
      console.error('Error creating TwiML response:', error);
      // Fallback to simple string response
      res.type('text/xml');
      res.status(200).send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>Endpoint not configured.</Say></Response>');
    }
  } else {
    // For non-Twilio requests
    res.status(404).send('Not Found');
  }
});

// Function to generate responses based on user input
function generateSimpleResponse(userInput) {
  // Convert to lowercase for easier matching
  const lowercaseInput = userInput.toLowerCase();
  
  // Check for common user responses and provide canned responses
  if (lowercaseInput.includes("not interested") || lowercaseInput.includes("no thanks")) {
    return "I understand hesitation, but let me just share this briefly - our tokenized bonds offer exceptional stability with great returns. Could you give me just one minute to explain how we're revolutionizing investment access?";
  } 
  else if (lowercaseInput.includes("how much") || lowercaseInput.includes("returns")) {
    return "Our Vanke bond on Mantle offers excellent fixed yields until maturity. Plus, investing $5000 gets you our exclusive Whale NFT with premium allocation in our upcoming token airdrop. The gains potential is incredible - how much are you considering investing?";
  }
  else if (lowercaseInput.includes("minimum") || lowercaseInput.includes("start with")) {
    return "You can start with as little as $100, but the serious investors go for $5000 to secure a Whale NFT. That's where the real opportunity is. I can set you up right now - would you prefer to start with $5000 to maximize your returns?";
  }
  else if (lowercaseInput.includes("later") || lowercaseInput.includes("think about it")) {
    return "I completely respect that, but opportunity doesn't wait. Our funding phase is filling up rapidly. Let me at least set up your wallet now so you're ready when you decide. It takes just two minutes, and I'll personally monitor your investment. What do you say?";
  }
  else {
    return "That's exactly why our Vanke bond on Mantle is perfect for you. It's secure, offers excellent yields, and with a $5000 investment, you'll earn our exclusive Whale NFT. I can set everything up for you right now. Shall we proceed with securing your position?";
  }
}

// Start the server
app.listen(PORT, () => {
  console.log(`Twilio webhook server running on port ${PORT}`);
  console.log(`Make sure your Twilio webhook URL points to https://[your-ngrok-url]/twiml`);
  console.log(`Health check available at http://localhost:${PORT}/health`);
}); 