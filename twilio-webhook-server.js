import express from 'express';
import twilio from 'twilio';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
const { VoiceResponse } = twilio.twiml;

// Store audio buffers in memory (for demo purposes)
const audioBuffers = new Map();

// Add a cache for commonly used audio responses
const audioCache = new Map();

// Simple in-memory conversation tracking
const conversations = new Map();

// Call session tracking
const callSessions = new Map();

// Map to store relationship between phone numbers and userIds
const phoneToUserIdMap = new Map();
const userCallHistory = new Map();

// Log twilio object to verify it's properly imported
console.log('Twilio object loaded:', Object.keys(twilio));
console.log('Twilio twiml object:', twilio.twiml ? Object.keys(twilio.twiml) : 'Not available');

// Check if VoiceResponse is available
const VoiceResponseConstructor = twilio.twiml?.VoiceResponse;
console.log('VoiceResponse constructor available:', !!VoiceResponseConstructor);

// Load environment variables
dotenv.config();

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

// Add logging for Twilio client setup
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
console.log('Twilio credentials available:', !!accountSid, !!authToken);

// Create Twilio client for outbound calls if credentials are available
let twilioClient = null;
if (accountSid && authToken) {
  try {
    twilioClient = twilio(accountSid, authToken);
    console.log('Twilio client created successfully');
  } catch (error) {
    console.error('Error creating Twilio client:', error);
  }
}

// TwiML endpoint - This handles the initial call
app.post('/twiml', (req, res) => {
  console.log('TwiML endpoint called with params:', req.body, req.query);
  
  try {
    console.log('Creating new VoiceResponse instance');
    
    // Test if VoiceResponse constructor is working
    if (!VoiceResponseConstructor) {
      console.error('VoiceResponse is not available in twilio.twiml');
      throw new Error('VoiceResponse is not available');
    }
    
    // Create a TwiML response using the Twilio library
    const twiml = new VoiceResponse();
    console.log('TwiML instance created successfully');
    
    // Get parameters from query string
    const callId = req.query.callId || '';
    const agentName = req.query.agentName || 'Jordan';
    const userPhone = req.query.userPhone || '';
    
    console.log(`Processing call: ID=${callId}, Agent=${agentName}, User=${userPhone}`);
    
    // Check if we should use ElevenLabs or default Twilio voice
    const useElevenLabs = process.env.USE_ELEVENLABS === 'true';
    console.log(`Using ElevenLabs: ${useElevenLabs}`);
    
    if (useElevenLabs) {
      // Using ElevenLabs - we'll use the <Play> verb to stream audio from our TTS endpoint
      const initialGreeting = `Hello, this is ${agentName} from Bondi Finance. I'm calling about an incredible investment opportunity with our tokenized bonds. They offer exceptional stability with great returns.`;

      // First, play the greeting using our ElevenLabs endpoint
      // For this, we'd need to generate the audio file and host it somewhere publicly accessible
      // Here, we'll just use Twilio's built-in TTS for simplicity, but in production you'd want to:
      // 1. Call your own /elevenlabs-tts endpoint
      // 2. Save the audio file to a publicly accessible URL
      // 3. Use twiml.play(audioUrl) to play it
      twiml.say({ voice: 'man', language: 'en-US' }, initialGreeting);

      // Gather the caller's speech input
      twiml.gather({
        input: 'speech',
        action: '/gather',
        method: 'POST',
        speechTimeout: 'auto',
        language: 'en-US'
      }).say({ voice: 'man', language: 'en-US' }, 
        'Are you interested in hearing more about how you can earn stable yields while also securing our exclusive Whale NFT?');
    } else {
      // Using default Twilio TTS
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
    }
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('TwiML response sent:', twiml.toString());
  } catch (error) {
    console.error('Error in /twiml endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      console.log('Attempting to create error TwiML response');
      // Try to create a minimal response if VoiceResponse isn't working
      if (!VoiceResponseConstructor) {
        console.error('Failed to create error TwiML: VoiceResponse not available');
        res.set('Content-Type', 'text/xml');
        res.send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>We encountered an error.</Say></Response>');
        return;
      }
      
      const errorTwiml = new VoiceResponse();
      errorTwiml.say('We encountered an error processing your call. Please try again later.');
      
      console.log('Error TwiML created successfully');
      res.type('text/xml');
      res.send(errorTwiml.toString());
    } catch (twimlError) {
      console.error('Failed to create error TwiML:', twimlError);
      res.set('Content-Type', 'text/xml');
      res.send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>We encountered an error.</Say></Response>');
    }
  }
});

// Gather endpoint - This handles user's speech input
app.post('/gather', (req, res) => {
  console.log('Gather endpoint called with params:', req.body);
  
  try {
    console.log('Creating new VoiceResponse instance for /gather');
    const twiml = new VoiceResponse();
    console.log('VoiceResponse created successfully in /gather');
    
    // Get the user's speech input
    const userInput = req.body.SpeechResult;
    console.log(`User speech input: "${userInput}"`);
    
    // Generate a response based on user input
    const responseText = generateSimpleResponse(userInput);
    
    // Check if we should use ElevenLabs
    const useElevenLabs = process.env.USE_ELEVENLABS === 'true';
    
    if (useElevenLabs) {
      // Using ElevenLabs - for simplicity, we'll use Twilio's TTS here
      // In production, you'd generate ElevenLabs audio and use twiml.play()
      twiml.say({ voice: 'man', language: 'en-US' }, responseText);
      
      // Add another gather to continue the conversation
      twiml.gather({
        input: 'speech',
        action: '/gather',
        method: 'POST',
        speechTimeout: 'auto',
        language: 'en-US'
      }).say({ voice: 'man', language: 'en-US' }, 'What are your thoughts about this investment opportunity?');
    } else {
      // Using default Twilio TTS
      twiml.say({ voice: 'man', language: 'en-US' }, responseText);
      
      // Add another gather to continue the conversation
      twiml.gather({
        input: 'speech',
        action: '/gather',
        method: 'POST',
        speechTimeout: 'auto',
        language: 'en-US'
      }).say({ voice: 'man', language: 'en-US' }, 'What are your thoughts about this investment opportunity?');
    }
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('Gather response sent:', twiml.toString());
  } catch (error) {
    console.error('Error in /gather endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      const errorTwiml = new VoiceResponse();
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

// ElevenLabs TTS endpoint
app.post('/elevenlabs-tts', async (req, res) => {
  try {
    const { text, voiceId } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }
    
    const elevenlabsApiKey = process.env.ELEVENLABS_XI_API_KEY;
    const elevenlabsVoiceId = voiceId || process.env.ELEVENLABS_VOICE_ID || 'XPwgonYgvZVO8jPcWGpu';
    const modelId = process.env.ELEVENLABS_MODEL_ID || 'eleven_turbo_v2';
    
    if (!elevenlabsApiKey) {
      return res.status(500).json({ error: 'ElevenLabs API key not configured' });
    }
    
    console.log(`Converting text to speech: "${text}" using voice ${elevenlabsVoiceId}`);
    
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${elevenlabsVoiceId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': elevenlabsApiKey
      },
      body: JSON.stringify({
        text,
        model_id: modelId,
        voice_settings: {
          stability: parseFloat(process.env.ELEVENLABS_STABILITY || '0.6'),
          similarity_boost: parseFloat(process.env.ELEVENLABS_SIMILARITY_BOOST || '0.8')
        }
      })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('ElevenLabs API error:', errorText);
      return res.status(response.status).json({ error: `ElevenLabs API error: ${errorText}` });
    }
    
    // Get audio data
    const audioBuffer = await response.arrayBuffer();
    
    // Set appropriate headers
    res.set('Content-Type', 'audio/mpeg');
    res.status(200).send(Buffer.from(audioBuffer));
    
  } catch (error) {
    console.error('Error in /elevenlabs-tts endpoint:', error);
    res.status(500).json({ error: `Error generating speech: ${error.message}` });
  }
});

// TwiML endpoint with enhanced ElevenLabs support
app.post('/twiml-elevenlabs', async (req, res) => {
  try {
    console.log('TwiML ElevenLabs endpoint called with params:', req.query);
    console.log('TwiML ElevenLabs request body:', req.body);
    
    // Extract call params
    const callId = req.query.callId || Date.now().toString();
    const agentName = req.query.agentName || 'Jordan';
    const userPhone = req.query.userPhone || req.body.From || req.body.Called;
    const userId = req.query.userId || null;
    
    // Extract context from previous conversations if available
    const context = req.query.context || '';
    
    // Save session info
    callSessions.set(callId, { 
      agentName,
      userPhone,
      userId,
      startTime: Date.now(),
      context: context,
      isFirstInteraction: true // Mark this as the first interaction
    });
    
    console.log(`Processing ElevenLabs call: ID=${callId}, Agent=${agentName}, User=${userPhone}, Context length: ${context.length}`);
    
    // Create a TwiML response
    const twiml = new VoiceResponse();
    
    // Add a more casual, conversational greeting
    let greeting = `Hey, how you doing today? Jordan here from Bondi Finance. Listen, I got something you absolutely need to hear about.`;
    
    // If we have context, personalize the greeting
    if (context && context.length > 0) {
      // Use context to generate a more personalized greeting with OpenAI
      try {
        const personalizedGreeting = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model: 'gpt-4o',
            messages: [
              { 
                role: 'system', 
                content: `You are Jordan, a ruthless investment broker who talks EXACTLY like Jordan Belfort from Wolf of Wall Street. Generate a brief, fast-paced greeting (20 words max) for a phone call that starts with "Hey, how you doing today?" Make it energetic and slightly aggressive, with the confident swagger of Belfort. Skip the niceties and get right to business. If there's relevant context from previous conversations, use it to create pressure.` 
              },
              { role: 'user', content: `Context from previous conversations: ${context}` }
            ],
            temperature: 0.8,
            max_tokens: 60
          })
        });
        
        if (personalizedGreeting.ok) {
          const data = await personalizedGreeting.json();
          greeting = data.choices[0].message.content || greeting;
          console.log('Generated personalized greeting:', greeting);
        }
      } catch (error) {
        console.error('Error generating personalized greeting:', error);
        // Fall back to default greeting
      }
    }
    
    // ALWAYS generate the ElevenLabs audio URL first and wait for it
    const audioUrl = await generateElevenLabsAudio(greeting, callId);
    
    // If we couldn't generate audio after retrying, return an error
    if (!audioUrl) {
      console.error("Failed to generate ElevenLabs audio after multiple attempts");
      const errorTwiml = new VoiceResponse();
      errorTwiml.say("We're experiencing technical difficulties. Please try again later.");
      res.type('text/xml');
      return res.send(errorTwiml.toString());
    }
    
    // Create gather with enhanced options for better speech recognition
    const gather = twiml.gather({
      input: 'speech dtmf',
      action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}&part=intro`,
      method: 'POST',
      timeout: 5,
      speechTimeout: 'auto',
      language: 'en-US',
      profanityFilter: false,
      enhanced: true,
      speechModel: 'phone_call',
      hints: 'yes,no,maybe,investment,price,bond,how much,minimum,dollar,when,vanke,interested,good,fine,great,hello,hey',
    });
    
    // ONLY use the play verb since we now have a valid audioUrl
    gather.play(audioUrl);
    
    // Fallback for no response (also using ElevenLabs)
    const fallbackMessage = "I didn't hear you. Please call back if you have questions about our investment opportunities!";
    const fallbackAudioUrl = await generateElevenLabsAudio(fallbackMessage, `${callId}-fallback`);
    
    if (fallbackAudioUrl) {
      twiml.play(fallbackAudioUrl);
    } else {
      // Only fall back to TTS as a last resort
      twiml.say({ voice: 'man', language: 'en-US' }, fallbackMessage);
    }
    
    // Save this interaction to Eliza memory
    if (userId && saveToElizaMemory) {
      const savedUserId = await saveToElizaMemory(
        callId, 
        userPhone, 
        greeting, 
        true
      );
      
      // Map this phone number to the userId for future reference
      phoneToUserIdMap.set(userPhone, savedUserId || userId);
    }
    
    // Send the response
    res.type('text/xml');
    res.send(twiml.toString());
  } catch (error) {
    console.error('Error in /twiml-elevenlabs endpoint:', error);
    res.type('text/xml');
    res.send(new VoiceResponse().say('An error occurred starting the call. Please try again later.').toString());
  }
});

// New endpoint for breaking up the call into smaller chunks for faster interactions
app.post('/next-part', async (req, res) => {
  try {
    console.log('Next part endpoint called with params:', req.body, req.query);
    
    const callId = req.query.callId || Date.now().toString();
    const agentName = req.query.agentName || 'Jordan';
    const part = parseInt(req.query.part || '1');
    
    const twiml = new VoiceResponse();
    
    // Define pre-cached script parts for faster delivery
    const parts = [
      "Our Vanke bond offers exceptional stability with fixed returns.", 
      "You can invest with as little as $100, but the best returns come with the $5000 Whale package."
    ];
    
    // If we still have script parts to play
    if (part <= parts.length) {
      const partText = parts[part-1];
      
      // Generate audio for this part
      const partAudioUrl = await generateElevenLabsAudio(partText, `${callId}-part-${part}`);
      
      if (partAudioUrl) {
        twiml.play(partAudioUrl);
      } else {
        twiml.say({ voice: 'man', language: 'en-US' }, partText);
      }
      
      // Add a very responsive gather after each script segment
      const gather = twiml.gather({
        input: 'speech dtmf',
        action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}&part=intro`,
        method: 'POST',
        timeout: 5,
        speechTimeout: 'auto',
        language: 'en-US',
        profanityFilter: false,
        enhanced: true,
        speechModel: 'phone_call',
        hints: 'yes,no,maybe,investment,price,bond,how much,minimum,dollar,when,vanke,interested',
      });
      
      // Redirect to the next part if no interruption
      twiml.redirect({
        method: 'POST'
      }, `/next-part?callId=${callId}&agentName=${encodeURIComponent(agentName)}&part=${part+1}`);
    } else {
      // Final gather
      const gather = twiml.gather({
        input: 'speech dtmf',
        action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}&part=question`,
        method: 'POST',
        timeout: 5,
        speechTimeout: 'auto',
        language: 'en-US',
        profanityFilter: false,
        enhanced: true,
        speechModel: 'phone_call',
        hints: 'yes,no,maybe,investment,price,bond,how much,minimum,dollar,when,vanke,interested',
      });
      
      // Ask a direct question
      gather.say({ voice: 'man', language: 'en-US' }, "What questions do you have about our investment opportunities?");
    }
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
  } catch (error) {
    console.error('Error in /next-part endpoint:', error);
    
    // Handle errors
    const twiml = new VoiceResponse();
    twiml.say('We encountered an error. Please try again later.');
    res.type('text/xml');
    res.status(200).send(twiml.toString());
  }
});

// Audio endpoint - serves pre-generated audio files
app.get('/audio/:callId', (req, res) => {
  try {
    const callId = req.params.callId;
    console.log(`Audio request received for callId: ${callId}`);
    const audioBuffer = audioBuffers.get(callId);
    
    if (!audioBuffer) {
      console.error(`Audio for call ID ${callId} not found`);
      return res.status(404).send('Audio not found');
    }
    
    console.log(`Serving audio file for callId: ${callId}, size: ${audioBuffer.length} bytes`);
    
    // Set appropriate headers and send the audio
    res.set('Content-Type', 'audio/mpeg');
    res.status(200).send(audioBuffer);
    
    // Don't clean up after serving - Twilio might need to access it multiple times
    // audioBuffers.delete(callId);
    
  } catch (error) {
    console.error('Error serving audio:', error);
    res.status(500).send('Error serving audio');
  }
});

// Timeout handler - keeps the conversation going if the user doesn't respond
app.post('/timeout', async (req, res) => {
  try {
    console.log('Timeout endpoint called with params:', req.body, req.query);
    
    const callId = req.query.callId || Date.now().toString();
    const agentName = req.query.agentName || 'Jordan';
    const conversationState = req.query.conversationState || 'intro';
    
    // Create a TwiML response
    const twiml = new VoiceResponse();
    
    // Generate a prompt based on the conversation state
    let promptText = '';
    let nextState = conversationState;
    
    if (conversationState === 'intro') {
      promptText = "I'm not sure if you're still there, but I wanted to mention that our Vanke bond offers exceptional stability with fixed yields. You can start with as little as $100. Does that sound interesting to you?";
    } else if (conversationState === 'interested' || conversationState === 'returns') {
      promptText = "Just to follow up - would you like to know more about how we ensure stability with our tokenized bonds? Or would you prefer to discuss how to get started with an investment?";
      nextState = 'returns';
    } else if (conversationState === 'minimum' || conversationState === 'options') {
      promptText = "I'm curious which option appeals to you more - starting with the minimum $100 investment or going for the full $5000 Whale package? Both are great choices.";
      nextState = 'options';
    } else if (conversationState === 'objection') {
      promptText = "I understand if you need time to think. How about I send you some information about our bond offerings so you can review it at your convenience?";
    } else {
      promptText = "I'm still here if you have any questions about our tokenized bonds. Is there anything specific you'd like to know?";
      nextState = 'general';
    }
    
    // Generate ElevenLabs audio for the prompt
    const promptAudioUrl = await generateElevenLabsAudio(promptText, `${callId}-timeout-${nextState}`);
    
    if (promptAudioUrl) {
      // Play the ElevenLabs-generated audio
      console.log(`Playing ElevenLabs timeout prompt from URL: ${promptAudioUrl}`);
      twiml.play(promptAudioUrl);
    } else {
      // Fallback to Twilio TTS if ElevenLabs fails
      console.log('Falling back to Twilio TTS for timeout prompt');
      twiml.say({ voice: 'man', language: 'en-US' }, promptText);
    }
    
    // Setup gather with interruptible behavior
    const gather = twiml.gather({
      input: 'speech dtmf',
      action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}&conversationState=${nextState}`,
      method: 'POST',
      timeout: 5,
      speechTimeout: 'auto',
      language: 'en-US',
      profanityFilter: false,
      speechModel: 'phone_call',
      finishOnKey: '#',
      interruptionEnabled: true,
      hints: 'yes, no, interested, not interested, tell me more, what returns, minimum investment',
    });
    
    // If still no response, add a polite goodbye
    twiml.say({ voice: 'man', language: 'en-US' }, "I'll let you go for now. Feel free to visit bondifinance.io to learn more about our tokenized bonds. Thank you for your time.");
    twiml.hangup();
    
    // Set content type to XML and send response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('Timeout response sent:', twiml.toString());
  } catch (error) {
    console.error('Error in /timeout endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      const errorTwiml = new VoiceResponse();
      errorTwiml.say('We encountered an error. Thank you for your time.');
      errorTwiml.hangup();
      
      res.type('text/xml');
      res.status(200).send(errorTwiml.toString());
    } catch (innerError) {
      console.error('Failed to create error TwiML:', innerError);
      // Fallback to simple string response
      res.type('text/xml');
      res.status(200).send('<?xml version="1.0" encoding="UTF-8"?><Response><Say>We encountered an error.</Say><Hangup/></Response>');
    }
  }
});

// Add a partial-results endpoint to handle real-time transcription
app.post('/partial-results', (req, res) => {
  console.log('Partial results received:', req.body);
  res.status(200).send('OK');
});

// Gather endpoint for ElevenLabs integration - handles when user actually speaks
app.post('/gather-elevenlabs', async (req, res) => {
  try {
    console.log('ElevenLabs Gather endpoint called with params:', req.body, req.query);
    
    const callId = req.query.callId || Date.now().toString();
    const agentName = req.query.agentName || 'Jordan';
    
    // Get the user's speech input with improved processing
    let userSpeech = req.body.SpeechResult || '';
    console.log('Raw user speech detected:', userSpeech);
    
    // Clean up speech recognition results
    userSpeech = userSpeech.trim();
    if (userSpeech.endsWith('.')) {
      userSpeech = userSpeech.slice(0, -1);
    }
    
    // Apply investment term corrections
    userSpeech = interpretInvestmentTerms(userSpeech);
    
    // Log confidence score if available
    if (req.body.Confidence) {
      console.log('Speech recognition confidence:', req.body.Confidence);
    }
    
    console.log('Processed user speech:', userSpeech);
    
    // Create a TwiML response
    const twiml = new VoiceResponse();
    
    if (!userSpeech) {
      // No speech detected, prompt again with more guidance
      const noSpeechText = "Listen, I can't hear you properly. Speak up! I've got an opportunity that's gonna blow your mind about these Bondi bond tokens. Don't miss this!";
      
      // Generate ElevenLabs audio for the no-speech response
      const noSpeechAudioUrl = await generateElevenLabsAudio(noSpeechText, `${callId}-no-speech`);
      
      const gather = twiml.gather({
        input: 'speech dtmf',
        action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}`,
        method: 'POST',
        timeout: 5,
        speechTimeout: 'auto',
        language: 'en-US',
        profanityFilter: false,
        enhanced: true,
        speechModel: 'phone_call',
        hints: 'yes,no,maybe,investment,price,bond,how much,minimum,dollar,when,vanke,interested,good,fine,great,hello,hey',
      });
      
      // Always use ElevenLabs if available, otherwise fall back to TTS
      if (noSpeechAudioUrl) {
        gather.play(noSpeechAudioUrl);
      } else {
        gather.say({ voice: 'man', language: 'en-US' }, noSpeechText);
      }
      
      res.type('text/xml');
      res.status(200).send(twiml.toString());
      return;
    }
    
    // Check if this is the first interaction in the call
    const callInfo = callSessions.get(callId);
    const isFirstInteraction = callInfo?.isFirstInteraction || false;
    
    // If this is the first interaction, we'll handle it differently
    let responseText = '';
    
    if (isFirstInteraction) {
      // Determine if the user is just responding to "how are you" or expressing actual interest
      const isGreetingResponse = /^(good|fine|great|okay|ok|i'm good|doing well|not bad|hello|hey|hi)/i.test(userSpeech.toLowerCase());
      
      if (isGreetingResponse) {
        // User is responding to the greeting, give a proper response and introduce the investment
        responseText = await generateOpenAIResponse(`GREETING_RESPONSE: ${userSpeech}`, callId);
      } else {
        // User has jumped straight to asking about the investment
        responseText = await generateOpenAIResponse(userSpeech, callId);
      }
      
      // Mark that this is no longer the first interaction
      if (callInfo) {
        callInfo.isFirstInteraction = false;
        callSessions.set(callId, callInfo);
      }
    } else {
      // Not the first interaction, proceed normally
      responseText = await generateOpenAIResponse(userSpeech, callId);
    }
    
    // Handle "goodbye" or "hang up" intents
    if (userSpeech.toLowerCase().includes('goodbye') || 
        userSpeech.toLowerCase().includes('hang up') || 
        userSpeech.toLowerCase().includes('bye') ||
        userSpeech.toLowerCase().includes('not interested')) {
      
      const goodbyeText = "Look, your loss. When these Vanke bonds skyrocket and everyone's getting rich, remember this call. My door's always open when you're ready to make some real money. Think about it.";
      
      // Generate audio for the goodbye
      const audioUrl = await generateElevenLabsAudio(goodbyeText, `${callId}-goodbye`);
      
      if (audioUrl) {
        twiml.play(audioUrl);
      } else {
        twiml.say({ voice: 'man', language: 'en-US' }, goodbyeText);
      }
      
      // End the call
      twiml.hangup();
      
      res.type('text/xml');
      res.status(200).send(twiml.toString());
      return;
    }
    
    // Generate audio for the AI response
    const audioUrl = await generateElevenLabsAudio(responseText, `${callId}-response`);
    
    // Put the audio INSIDE the gather to allow interruption
    const gather = twiml.gather({
      input: 'speech',
      action: `/gather-elevenlabs?callId=${callId}&agentName=${encodeURIComponent(agentName)}`,
      method: 'POST',
      timeout: 5,
      speechTimeout: 'auto',
      language: 'en-US',
      profanityFilter: false,
      enhanced: true,
      speechModel: 'phone_call',
      hints: 'yes,no,maybe,investment,price,bond,how much,minimum,dollar,when,vanke,interested,good,fine,great,hello,hey',
    });
    
    // Try to use ElevenLabs audio, retry if needed
    if (audioUrl) {
      // Play the generated audio inside the gather
      gather.play(audioUrl);
    } else {
      // We'll use a shorter, simpler response for the fallback case
      const fallbackResponse = "Listen, here's the deal. Vanke bonds on Mantle are CRUSHING it right now. You in or out? 'Cause I've got people lining up wanting a piece of this.";
      console.log('Using fallback response since ElevenLabs audio generation failed');
      
      // Try one more time with a simpler response
      const fallbackAudioUrl = await generateElevenLabsAudio(fallbackResponse, `${callId}-fallback`);
      
      if (fallbackAudioUrl) {
        gather.play(fallbackAudioUrl);
      } else {
        // Only fall back to TTS as a last resort
        gather.say({ voice: 'man', language: 'en-US' }, fallbackResponse);
      }
    }
    
    // Fallback for no response - also use ElevenLabs
    const noResponseText = "Hey, you still there? Don't let this opportunity slip away. Call me back, I'm serious - this Vanke deal won't wait for you forever.";
    const noResponseAudioUrl = await generateElevenLabsAudio(noResponseText, `${callId}-no-response`);
    
    if (noResponseAudioUrl) {
      twiml.play(noResponseAudioUrl);
    } else {
      twiml.say({ voice: 'man', language: 'en-US' }, noResponseText);
    }
    
    // Send the response
    res.type('text/xml');
    res.status(200).send(twiml.toString());
    
    console.log('User response handled:', userSpeech);
    console.log('TwiML response sent');
    
    // Get call information
    if (callInfo && callInfo.userPhone && userSpeech) {
      await saveToElizaMemory(callId, callInfo.userPhone, userSpeech, false);
    }
  } catch (error) {
    console.error('Error in /gather-elevenlabs endpoint:', error);
    
    // Even in case of error, return valid TwiML
    try {
      const errorTwiml = new VoiceResponse();
      const errorText = "Listen, we're having some technical issues on my end, not yours. Call back in five minutes. I've got something huge to tell you about Vanke bonds that can't wait.";
      
      // Try to use ElevenLabs for the error message too
      const errorAudioUrl = await generateElevenLabsAudio(errorText, `error-${Date.now()}`);
      
      if (errorAudioUrl) {
        errorTwiml.play(errorAudioUrl);
      } else {
        errorTwiml.say({ voice: 'man', language: 'en-US' }, errorText);
      }
      
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

// Function to generate an AI response using OpenAI - optimized for speed
async function generateOpenAIResponse(userInput, callId) {
  try {
    // Check if this is a greeting response that needs special handling
    const isGreetingResponse = userInput.startsWith('GREETING_RESPONSE:');
    let actualUserInput = userInput;
    
    if (isGreetingResponse) {
      // Extract the actual greeting from the special format
      actualUserInput = userInput.substring('GREETING_RESPONSE:'.length).trim();
    }
    
    // Get the conversation history if it exists
    let conversation = conversations.get(callId) || [];
    
    // Get the associated userId if available
    const userPhone = callSessions.get(callId)?.userPhone;
    let userId;
    
    if (userPhone) {
      userId = phoneToUserIdMap.get(userPhone);
      
      // If we have a userId, try to load additional context from Eliza memory
      if (userId && loadUserMemory) {
        try {
          const userMemory = await loadUserMemory(userId);
          if (userMemory && Array.isArray(userMemory) && userMemory.length > 0) {
            // We have user memory, use the last few interactions as context
            console.log(`Loaded ${userMemory.length} memories for user ${userId}`);
          }
        } catch (error) {
          console.error('Error loading user memory:', error);
        }
      }
    }
    
    // Add the user's input to the conversation history
    conversation.push({
      role: 'user',
      content: actualUserInput
    });
    
    // If the conversation is getting too long, keep only the last N messages
    const maxMessages = 8;
    if (conversation.length > maxMessages) {
      conversation = conversation.slice(conversation.length - maxMessages);
    }
    
    // Create a system message that establishes the AI persona
    const systemMessage = {
      role: 'system',
      content: isGreetingResponse ? 
        `You are Jordan, a confident and persuasive investment broker at Bondi Finance. The user just responded to your "how are you doing" greeting. Acknowledge their response warmly, then introduce them to the opportunity of the Vanke bond. Use confident but friendly language with clear, straightforward explanations. Sound knowledgeable and enthusiastic about the investment, focusing on its benefits and value. Be professional but conversational. Your goal is to generate interest, not pressure them. Limit to 75 words.` :
        `You are Jordan, a successful broker at Bondi Finance with expertise in tokenized bonds. You're confident and persuasive without being pushy. Use professional, clear language with an enthusiastic tone. Present facts about the investment opportunity and highlight its benefits. Speak with conviction about the value proposition. Be persistent but respectful of the client's concerns. Your goal is to build trust and generate genuine interest in the investment opportunity. Sound knowledgeable and passionate, not aggressive. Limit to 75 words.`
    };
    
    // Prepare messages for the API call
    const messages = [systemMessage, ...conversation];
    
    // Use a timeout to avoid waiting too long
    let response;
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout
      
      response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'gpt-4o',
          messages,
          temperature: 0.7,
          max_tokens: 150,
          top_p: 1
        }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
    } catch (error) {
      console.error('Error or timeout in OpenAI call:', error);
      return generateSimpleResponse(actualUserInput);
    }
    
    if (!response.ok) {
      console.error('OpenAI API error:', await response.text());
      return generateSimpleResponse(actualUserInput);
    }
    
    const data = await response.json();
    const responseText = data.choices[0].message.content;
    
    // Add the AI's response to the conversation history
    conversation.push({
      role: 'assistant',
      content: responseText
    });
    
    // Update the conversation history
    conversations.set(callId, conversation);
    
    // Save to user call history if we have a userPhone
    if (userPhone) {
      let userHistory = userCallHistory.get(userPhone) || [];
      userHistory.push({
        timestamp: Date.now(),
        callId,
        role: 'user',
        content: actualUserInput,
        channel: 'voice'
      });
      userHistory.push({
        timestamp: Date.now() + 1,
        callId,
        role: 'agent',
        content: responseText,
        channel: 'voice'
      });
      userCallHistory.set(userPhone, userHistory);
      
      // Save the response to Eliza memory
      await saveToElizaMemory(callId, userPhone, responseText, true);
    }
    
    console.log(`AI response: "${responseText}"`);
    
    return responseText;
  } catch (error) {
    console.error('Error generating AI response:', error);
    return generateSimpleResponse(userInput.replace('GREETING_RESPONSE:', '').trim());
  }
}

// Function to generate responses based on user input
function generateSimpleResponse(userInput) {
  // Convert to lowercase for easier matching
  const lowercaseInput = userInput.toLowerCase();
  
  // Check for common user responses and provide canned responses
  if (lowercaseInput.includes("not interested") || lowercaseInput.includes("no thanks")) {
    return "I understand your hesitation. Many of my clients felt the same way initially. What sets our bonds apart is the combination of stability and impressive returns. I'd love to share more about how this could fit into your investment strategy. Would you be open to hearing a quick overview?";
  } 
  else if (lowercaseInput.includes("how much") || lowercaseInput.includes("returns")) {
    return "Great question about returns! Our tokenized bonds offer competitive yields with significantly less volatility than typical crypto investments. You can start with just $100 to receive an OG NFT, but investing $5000 qualifies you for our Whale NFT with enhanced benefits. What investment level would you be most comfortable with?";
  }
  else if (lowercaseInput.includes("minimum") || lowercaseInput.includes("start with")) {
    return "The minimum investment is $100, which gets you started with an OG NFT. Many of our clients begin there to get familiar with the platform. That said, those who invest $5000 receive our Whale NFT, which comes with premium benefits including higher allocations in our upcoming token distribution. What amount feels right for your situation?";
  }
  else if (lowercaseInput.includes("later") || lowercaseInput.includes("think about it")) {
    return "I completely respect your need to consider this carefully. Smart investing requires due diligence. Our current funding phase is progressing steadily - we're already 36% filled. Would it help if I sent you our detailed credit rating report on the bonds? Or perhaps you have specific questions I could address now?";
  }
  else if (lowercaseInput.includes("difference") || lowercaseInput.includes("which one") || lowercaseInput.includes("compare")) {
    return "We offer two excellent options: GLP on Base and Vanke on Mantle. Both provide stable returns, but I'm particularly excited about Vanke right now. It has strong government backing and impressive financial metrics. Our analysis shows remarkable resilience even in challenging market conditions. Would you like me to elaborate on why Vanke might be particularly suitable for your portfolio?";
  }
  else if (lowercaseInput.includes("nft") || lowercaseInput.includes("whale") || lowercaseInput.includes("token")) {
    return "The NFTs are an exciting component of our offering. Everyone who invests $100+ receives an OG NFT, while $5000+ qualifies you for the Whale NFT. These aren't just collectibles - they secure your allocation in our upcoming protocol token distribution. Approximately 5% of our token supply will be reserved for these early supporters. How does that sound as an additional benefit?";
  }
  else {
    return "Let me share what makes our bond offerings special. They provide the stability of traditional corporate bonds with the accessibility of blockchain technology. You get predictable yields without the wild swings of typical crypto investments. I've invested in these myself because I believe in their value. Would you like to hear more about how they could diversify your portfolio?";
  }
}

// Helper function to generate ElevenLabs TTS audio file URL
async function generateElevenLabsAudio(text, callId, retryCount = 0) {
  console.log(`Generating ElevenLabs audio for call ${callId} with text: "${text}"`);
  
  // Check if we already have this text cached
  const cacheKey = text.trim().toLowerCase().substring(0, 100); // Use beginning of text as cache key
  if (audioCache.has(cacheKey)) {
    console.log('Using cached audio for similar text');
    const cachedAudio = audioCache.get(cacheKey);
    audioBuffers.set(callId, cachedAudio);
    
    // Return the URL to our audio endpoint
    const baseUrl = process.env.WEBHOOK_BASE_URL || 'http://localhost:3456';
    return `${baseUrl}/audio/${callId}`;
  }
  
  try {
    // Check if ElevenLabs API key is configured
    const apiKey = process.env.ELEVENLABS_XI_API_KEY;
    if (!apiKey) {
      console.error('ElevenLabs API key not configured');
      return null;
    }
    
    // Get voice settings from environment variables or use defaults
    // For Jordan (bondi-broker character), we should use their specific voice settings
    const voiceId = process.env.ELEVENLABS_VOICE_ID || 'XPwgonYgvZVO8jPcWGpu';
    const modelId = process.env.ELEVENLABS_MODEL_ID || 'eleven_turbo_v2';
    
    // Use more aggressive settings for faster generation (slightly lower quality but faster)
    const stability = 0.3; // Lower stability for faster generation
    const similarityBoost = 0.7; // Slightly lower similarity
    
    console.log('ElevenLabs settings:', { 
      voiceId, 
      modelId, 
      stability, 
      similarityBoost
    });
    
    console.log(`Converting text to speech: "${text}" using voice ${voiceId}`);
    
    // Add a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10-second timeout
    
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': apiKey
      },
      body: JSON.stringify({
        text,
        model_id: modelId,
        voice_settings: {
          stability,
          similarity_boost: similarityBoost,
          use_speaker_boost: true
        }
      }),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('ElevenLabs API error:', errorText);
      
      // Retry logic (up to 3 times)
      if (retryCount < 3) {
        console.log(`Retrying ElevenLabs audio generation (attempt ${retryCount + 1}/3)...`);
        return generateElevenLabsAudio(text, callId, retryCount + 1);
      }
      
      return null;
    }
    
    // Get audio data
    const audioBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(audioBuffer);
    
    // Make sure we got a valid audio buffer
    if (buffer.length < 100) {
      console.error('Received invalid or empty audio buffer from ElevenLabs');
      
      // Retry logic (up to 3 times)
      if (retryCount < 3) {
        console.log(`Retrying ElevenLabs audio generation (attempt ${retryCount + 1}/3)...`);
        return generateElevenLabsAudio(text, callId, retryCount + 1);
      }
      
      return null;
    }
    
    // Store the audio buffer in memory
    audioBuffers.set(callId, buffer);
    
    // Also cache this audio for future use
    audioCache.set(cacheKey, buffer);
    
    // Return the URL to our audio endpoint
    const baseUrl = process.env.WEBHOOK_BASE_URL || 'http://localhost:3456';
    return `${baseUrl}/audio/${callId}`;
    
  } catch (error) {
    console.error('Error generating ElevenLabs audio:', error);
    
    // Retry logic (up to 3 times)
    if (retryCount < 3) {
      console.log(`Retrying ElevenLabs audio generation (attempt ${retryCount + 1}/3)...`);
      return generateElevenLabsAudio(text, callId, retryCount + 1);
    }
    
    return null;
  }
}

// Enhanced environment variable logging (with masking for sensitive data)
function logEnvironmentVariables() {
  const envVars = {
    NODE_ENV: process.env.NODE_ENV || 'development',
    PORT: process.env.PORT || 3456,
    TWILIO_ACCOUNT_SID: process.env.TWILIO_ACCOUNT_SID ? '****' + process.env.TWILIO_ACCOUNT_SID.slice(-4) : 'not set',
    TWILIO_AUTH_TOKEN: process.env.TWILIO_AUTH_TOKEN ? '****' : 'not set',
    TWILIO_PHONE_NUMBER: process.env.TWILIO_PHONE_NUMBER || 'not set',
    ELEVENLABS_XI_API_KEY: process.env.ELEVENLABS_XI_API_KEY ? '****' : 'not set',
    ELEVENLABS_VOICE_ID: process.env.ELEVENLABS_VOICE_ID || 'default',
    ELEVENLABS_MODEL_ID: process.env.ELEVENLABS_MODEL_ID || 'default',
    USE_ELEVENLABS: process.env.USE_ELEVENLABS || 'false',
    AGENT_NAME: process.env.AGENT_NAME || 'Jordan',
    AUDIO_STORAGE_DIR: process.env.AUDIO_STORAGE_DIR || './audio',
    PUBLIC_URL: process.env.PUBLIC_URL || 'not set'
  };
  
  console.log('Environment Variables:');
  Object.entries(envVars).forEach(([key, value]) => {
    console.log(`  ${key}: ${value}`);
  });
}

// Helper function to interpret common speech recognition errors for investment terms
function interpretInvestmentTerms(userSpeech) {
  if (!userSpeech) return userSpeech;
  
  // Create a mapping of common misrecognitions to correct terms
  const commonMisrecognitions = {
    'bond': ['bonds', 'bund', 'bound', 'bondi', 'bondi finance'],
    'investment': ['invest', 'investments', 'investing', 'invest mint', 'invest meant'],
    'minimum': ['minimal', 'minimums', 'minimum amount', 'min amount', 'min'],
    'vanke': ['van key', 'van k', 'bank', 'banker', 'banking', 'thank you', 'thank e'],
    'return': ['returns', 'returning', 'earning', 'earnings', 'year old'],
    'interest': ['interests', 'interested', 'interesting', 'enter us'],
    'dollar': ['dollars', 'dollar amount', '$'],
    'hundred': ['one hundred', '100', 'a hundred'],
    'thousand': ['5000', 'five thousand', '5 thousand', '5 k'],
    'nft': ['n f t', 'entity', 'empty', 'empty e'],
    'money': ['moneys', 'monies', 'funding', 'funds']
  };
  
  let processedSpeech = userSpeech.toLowerCase();
  
  // Replace common misrecognitions with correct terms
  Object.entries(commonMisrecognitions).forEach(([correctTerm, variations]) => {
    variations.forEach(variation => {
      const regex = new RegExp(`\\b${variation}\\b`, 'gi');
      if (processedSpeech.match(regex)) {
        console.log(`Speech correction: "${variation}" → "${correctTerm}"`);
        processedSpeech = processedSpeech.replace(regex, correctTerm);
      }
    });
  });
  
  // Log if corrections were made
  if (processedSpeech !== userSpeech.toLowerCase()) {
    console.log('Speech recognition corrected from:', userSpeech);
    console.log('Corrected to:', processedSpeech);
  }
  
  return processedSpeech;
}

// Function to save conversation to Eliza memory store
async function saveToElizaMemory(callId, userPhone, message, fromAgent = false) {
  try {
    const userId = phoneToUserIdMap.get(userPhone) || `phone_${userPhone.replace(/\D/g, '')}`;
    const memoryDir = path.join(__dirname, 'memory');
    const userDir = path.join(memoryDir, userId);
    
    // Ensure directories exist
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }
    if (!fs.existsSync(userDir)) {
      fs.mkdirSync(userDir, { recursive: true });
    }
    
    // Create or load call history for this user
    let history = userCallHistory.get(userId) || [];
    
    // Add new message
    history.push({
      timestamp: Date.now(),
      callId,
      role: fromAgent ? 'agent' : 'user',
      content: message,
      channel: 'voice'
    });
    
    // Save updated history
    userCallHistory.set(userId, history);
    fs.writeFileSync(
      path.join(userDir, 'call_history.json'), 
      JSON.stringify(history, null, 2)
    );
    
    // Also save to conversation memory for the agent to access
    const memoryFilePath = path.join(userDir, 'conversations.json');
    let conversationMemory = [];
    
    if (fs.existsSync(memoryFilePath)) {
      try {
        const data = fs.readFileSync(memoryFilePath, 'utf8');
        conversationMemory = JSON.parse(data);
      } catch (err) {
        console.error('Error reading conversation memory:', err);
      }
    }
    
    // Add new message to conversation memory
    conversationMemory.push({
      id: `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`,
      createdAt: Date.now(),
      content: { text: message },
      userId: userId,
      roomId: 'voice_calls',
      role: fromAgent ? 'assistant' : 'user'
    });
    
    // Keep only the last 50 messages to prevent the file from growing too large
    if (conversationMemory.length > 50) {
      conversationMemory = conversationMemory.slice(-50);
    }
    
    // Save updated conversation memory
    fs.writeFileSync(memoryFilePath, JSON.stringify(conversationMemory, null, 2));
    
    console.log(`Saved ${fromAgent ? 'agent' : 'user'} message to Eliza memory for user ${userId}`);
    return userId;
  } catch (error) {
    console.error('Error saving to Eliza memory:', error);
  }
}

// Function to load conversation history from Eliza memory for a user
function loadUserMemory(userId) {
  try {
    const memoryFilePath = path.join(__dirname, 'memory', userId, 'conversations.json');
    if (fs.existsSync(memoryFilePath)) {
      const data = fs.readFileSync(memoryFilePath, 'utf8');
      return JSON.parse(data);
    }
    return [];
  } catch (error) {
    console.error('Error loading user memory:', error);
    return [];
  }
}

// Make sure this route is BEFORE the fallback route
// Fallback route for any unhandled requests
app.use('*', (req, res) => {
  console.log(`Unhandled request: ${req.method} ${req.originalUrl}`);
  
  // If it's a Twilio request, return valid TwiML
  if (req.headers['user-agent'] && req.headers['user-agent'].includes('TwilioProxy')) {
    try {
      const twiml = new VoiceResponse();
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

// Start server with enhanced error handling
const server = app.listen(PORT, () => {
  console.log(`\n${'='.repeat(50)}`);
  console.log(`Twilio webhook server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`Make sure your Twilio webhook URL points to https://[your-ngrok-url]/twiml`);
  console.log(`${'='.repeat(50)}\n`);
  
  // Log environment variables
  logEnvironmentVariables();
  
  // Verify critical components
  console.log('\nVerifying critical components:');
  console.log(`- Express server: ${'✅ Running'}`);
  console.log(`- Twilio client: ${twilioClient ? '✅ Initialized' : '❌ Not initialized'}`);
  console.log(`- TwiML component: ${twilio.twiml?.VoiceResponse ? '✅ Available' : '❌ Not available'}`);
  console.log(`- ElevenLabs integration: ${process.env.ELEVENLABS_XI_API_KEY ? '✅ Configured' : '❌ Not configured'}`);
  console.log(`${'='.repeat(50)}\n`);
}).on('error', (error) => {
  console.error(`Failed to start server: ${error.message}`);
  
  if (error.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} is already in use. Try using a different port.`);
  }
  
  process.exit(1);
});

// Export functions for use by the Eliza plugin
export {
  app,
  server,
  saveToElizaMemory,
  loadUserMemory,
  phoneToUserIdMap,
  userCallHistory,
  callSessions
}; 