require('dotenv').config();
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { Readable } = require('stream');

// Configuration from environment
const ELEVENLABS_API_KEY = process.env.ELEVENLABS_XI_API_KEY;
const ELEVENLABS_VOICE_ID = process.env.ELEVENLABS_VOICE_ID || 'XPwgonYgvZVO8jPcWGpu';
const ELEVENLABS_MODEL_ID = process.env.ELEVENLABS_MODEL_ID || 'eleven_turbo_v2';
const ELEVENLABS_STABILITY = parseFloat(process.env.ELEVENLABS_STABILITY || '0.6');
const ELEVENLABS_SIMILARITY_BOOST = parseFloat(process.env.ELEVENLABS_SIMILARITY_BOOST || '0.8');

// Check audio-tests directory exists
const audioDir = path.join(__dirname, 'audio-tests');
if (!fs.existsSync(audioDir)) {
  fs.mkdirSync(audioDir, { recursive: true });
  console.log(`Created audio tests directory at ${audioDir}`);
}

/**
 * Convert text to speech using ElevenLabs API
 * @param {string} text - The text to convert to speech
 * @param {object} options - Voice options
 * @returns {Promise<Buffer>} - Audio buffer
 */
async function textToSpeech(text, options = {}) {
  const voiceId = options.voiceId || ELEVENLABS_VOICE_ID;
  const modelId = options.modelId || ELEVENLABS_MODEL_ID;
  const stability = options.stability || ELEVENLABS_STABILITY;
  const similarityBoost = options.similarityBoost || ELEVENLABS_SIMILARITY_BOOST;

  console.log(`Converting text to speech with ElevenLabs...`);
  console.log(`Voice ID: ${voiceId}`);
  console.log(`Model ID: ${modelId}`);
  console.log(`Stability: ${stability}`);
  console.log(`Similarity Boost: ${similarityBoost}`);

  try {
    const response = await axios({
      method: 'POST',
      url: `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      headers: {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': ELEVENLABS_API_KEY
      },
      data: {
        text,
        model_id: modelId,
        voice_settings: {
          stability,
          similarity_boost: similarityBoost
        }
      },
      responseType: 'arraybuffer'
    });

    return Buffer.from(response.data);
  } catch (error) {
    console.error('Error generating speech:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * Get available voices from ElevenLabs
 */
async function getVoices() {
  try {
    const response = await axios({
      method: 'GET',
      url: 'https://api.elevenlabs.io/v1/voices',
      headers: {
        'Accept': 'application/json',
        'xi-api-key': ELEVENLABS_API_KEY
      }
    });

    console.log('Available voices:');
    console.table(response.data.voices.map(voice => ({
      name: voice.name,
      voice_id: voice.voice_id
    })));
  } catch (error) {
    console.error('Error fetching voices:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * Save audio buffer to file
 * @param {Buffer} audioBuffer - The audio buffer to save
 * @param {string} filename - The filename to save to
 */
function saveAudioToFile(audioBuffer, filename) {
  const filePath = path.join(audioDir, filename);
  fs.writeFileSync(filePath, audioBuffer);
  console.log(`Audio saved to ${filePath}`);
}

/**
 * Main function to test ElevenLabs integration
 */
async function main() {
  console.log('Testing ElevenLabs integration...');

  // Verify API Key
  if (!ELEVENLABS_API_KEY) {
    console.error('ElevenLabs API key is missing. Please set the ELEVENLABS_XI_API_KEY environment variable.');
    process.exit(1);
  }

  try {
    // Test connection by listing available voices
    await getVoices();

    // Sample sales pitch for the Bondi Finance Wolf
    const salesPitch = `
    Listen, I want to be completely straight with you. This btGLP bond is the HOTTEST opportunity 
    in the market right now. You're getting GUARANTEED yields while traditional bonds are giving you 
    what, 4-5%? That's NOTHING! Plus, with just a $5,000 investment, you get our exclusive WHALE 
    NFT that guarantees you priority allocation in our future token airdrop. The funding phase only 
    has 28 days left, and we're already 15% filled. Smart money doesn't wait. So let me ask you directly - 
    how much are you looking to invest today?`;

    // Generate speech
    console.log('Generating sales pitch audio...');
    const audioBuffer = await textToSpeech(salesPitch.trim());
    
    // Save to file
    saveAudioToFile(audioBuffer, 'bondi-wolf-test.mp3');

    console.log('✅ Test completed successfully!');
  } catch (error) {
    console.error('❌ Test failed:', error);
    process.exit(1);
  }
}

// Run the test
main(); 