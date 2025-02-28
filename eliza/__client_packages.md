# 🔌 Client Packages
Source: https://elizaos.github.io/eliza/docs/packages/clients/

📦 PackagesClient PackagesOn this page🔌 Client Packages
Overview​
Eliza's client packages enable integration with various platforms and services. Each client provides a standardized interface for sending and receiving messages, handling media, and interacting with platform-specific features.
Architecture Overview​

Available Clients​

Discord (@elizaos/client-discord) - Full Discord bot integration
Twitter (@elizaos/client-twitter) - Twitter bot and interaction handling
Telegram (@elizaos/client-telegram) - Telegram bot integration
Direct (@elizaos/client-direct) - Direct API for custom integrations
Auto (@elizaos/client-auto) - Automated trading and interaction client
Alexa skill (@elizaos/client-alexa) - Alexa skill API integration


Installation​
# Discordpnpm add @elizaos/client-discord# Twitterpnpm add @elizaos/client-twitter# Telegrampnpm add @elizaos/client-telegram# Direct APIpnpm add @elizaos/client-direct# Auto Clientpnpm add @elizaos/client-auto

Discord Client​
The Discord client provides full integration with Discord's features including voice, reactions, and attachments.
Basic Setup​
import { DiscordClientInterface } from "@elizaos/client-discord";// Initialize clientconst client = await DiscordClientInterface.start(runtime);// Configuration in .envDISCORD_APPLICATION_ID = your_app_id;DISCORD_API_TOKEN = your_bot_token;
Features​

Voice channel integration
Message attachments
Reactions handling
Media transcription
Room management

Voice Integration​
class VoiceManager {    // Join a voice channel    async handleJoinChannelCommand(interaction) {        await this.joinVoiceChannel(channel);    }    // Handle voice state updates    async handleVoiceStateUpdate(oldState, newState) {        if (newState.channelId) {            await this.handleUserJoinedChannel(newState);        }    }}
Message Handling​
class MessageManager {    async handleMessage(message) {        // Ignore bot messages        if (message.author.bot) return;        // Process attachments        if (message.attachments.size > 0) {            await this.processAttachments(message);        }        // Generate response        await this.generateResponse(message);    }}
Twitter Client​
The Twitter client enables posting, searching, and interacting with Twitter users.
Basic Setup​
import { TwitterClientInterface } from "@elizaos/client-twitter";// Initialize clientconst client = await TwitterClientInterface.start(runtime);// Configuration in .envTWITTER_USERNAME = your_username;TWITTER_PASSWORD = your_password;TWITTER_EMAIL = your_email;
Components​

PostClient: Handles creating and managing posts
SearchClient: Handles search functionality
InteractionClient: Manages user interactions

Post Management​
class TwitterPostClient {    async createPost(content: string) {        return await this.post({            text: content,            media: await this.processMedia(),        });    }    async replyTo(tweetId: string, content: string) {        return await this.post({            text: content,            reply: { in_reply_to_tweet_id: tweetId },        });    }}
Search Features​
class TwitterSearchClient {    async searchTweets(query: string) {        return await this.search({            query,            filters: {                recency: "recent",                language: "en",            },        });    }}
Telegram Client​
The Telegram client provides messaging and bot functionality for Telegram.
Basic Setup​
import { TelegramClientInterface } from "@elizaos/client-telegram";// Initialize clientconst client = await TelegramClientInterface.start(runtime);// Configuration in .envTELEGRAM_BOT_TOKEN = your_bot_token;
Message Management​
class TelegramClient {    async handleMessage(message) {        // Process message content        const content = await this.processMessage(message);        // Generate response        const response = await this.generateResponse(content);        // Send response        await this.sendMessage(message.chat.id, response);    }}
Direct Client​
The Direct client provides a REST API interface for custom integrations.
Basic Setup​
import { DirectClientInterface } from "@elizaos/client-direct";// Initialize clientconst client = await DirectClientInterface.start(runtime);
API Endpoints​
class DirectClient {    constructor() {        // Message endpoint        this.app.post("/:agentId/message", async (req, res) => {            const response = await this.handleMessage(req.body);            res.json(response);        });        // Image generation endpoint        this.app.post("/:agentId/image", async (req, res) => {            const images = await this.generateImage(req.body);            res.json(images);        });    }}
Auto Client​
The Auto client enables automated interactions and trading.
Basic Setup​
import { AutoClientInterface } from "@elizaos/client-auto";// Initialize clientconst client = await AutoClientInterface.start(runtime);
Automated Trading​
class AutoClient {    constructor(runtime: IAgentRuntime) {        this.runtime = runtime;        // Start trading loop        this.interval = setInterval(() => {            this.makeTrades();        }, 60 * 60 * 1000); // 1 hour interval    }    async makeTrades() {        // Get recommendations        const recommendations = await this.getHighTrustRecommendations();        // Analyze tokens        const analysis = await this.analyzeTokens(recommendations);        // Execute trades        await this.executeTrades(analysis);    }}
Alexa Client​
The Alexa client provides API integration with alexa skill.
Basic Setup​
import { AlexaClientInterface } from "@elizaos/client-alexa";// Initialize clientconst client = await AlexaClientInterface.start(runtime);// Configuration in .envALEXA_SKILL_ID= your_alexa_skill_idALEXA_CLIENT_ID= your_alexa_client_id #Alexa developer console permissions tabALEXA_CLIENT_SECRET= your_alexa_client_secret #Alexa developer console permissions tab
Common Features​
Message Handling​
All clients implement standard message handling:
interface ClientInterface {    handleMessage(message: Message): Promise<void>;    generateResponse(context: Context): Promise<Response>;    sendMessage(destination: string, content: Content): Promise<void>;}
Media Processing​
interface MediaProcessor {    processImage(image: Image): Promise<ProcessedImage>;    processVideo(video: Video): Promise<ProcessedVideo>;    processAudio(audio: Audio): Promise<ProcessedAudio>;}
Error Handling​
class BaseClient {    protected async handleError(error: Error) {        console.error("Client error:", error);        if (error.code === "RATE_LIMIT") {            await this.handleRateLimit(error);        } else if (error.code === "AUTH_FAILED") {            await this.refreshAuth();        }    }}

Best Practices​


Authentication

Store credentials securely in environment variables
Implement token refresh mechanisms
Handle authentication errors gracefully



Rate Limiting

Implement exponential backoff
Track API usage
Queue messages during rate limits



Error Handling

Log errors with context
Implement retry logic
Handle platform-specific errors



Media Processing

Validate media before processing
Handle different file formats
Implement size limits



Error Handling​
class BaseClient {    protected async handleError(error: Error) {        if (error.code === "RATE_LIMIT") {            await this.handleRateLimit(error);        } else if (error.code === "AUTH_FAILED") {            await this.refreshAuth();        } else if (error.code === "NETWORK_ERROR") {            await this.reconnect();        }        // Log error        console.error("Client error:", {            type: error.name,            message: error.message,            code: error.code,            stack: error.stack,        });    }}
Resource Management​
class ClientManager {    private async cleanup() {        // Close connections        await Promise.all(this.connections.map((conn) => conn.close()));        // Clear caches        this.cache.clear();        // Cancel timers        this.timers.forEach((timer) => clearInterval(timer));    }    private async reconnect() {        await this.cleanup();        await wait(this.calculateBackoff());        await this.initialize();    }}
Rate Limiting​
class RateLimiter {    private async handleRateLimit(error: RateLimitError) {        const delay = this.calculateBackoff(error);        await wait(delay);        return this.retryRequest();    }    private calculateBackoff(error: RateLimitError): number {        return Math.min(            this.baseDelay * Math.pow(2, this.attempts),            this.maxDelay        );    }}

Performance Optimization​
Connection Management​
class ClientManager {    private reconnect() {        await this.disconnect();        await wait(this.backoff());        await this.connect();    }}
Message Queuing​
class MessageQueue {    async queueMessage(message: Message) {        await this.queue.push(message);        this.processQueue();    }}
Troubleshooting​
Common Issues​

Authentication Failures

// Implement token refreshasync refreshAuth() {  const newToken = await this.requestNewToken();  await this.updateToken(newToken);}

Rate Limits

// Handle rate limitingasync handleRateLimit(error) {  const delay = this.calculateBackoff(error);  await wait(delay);  return this.retryRequest();}

Connection Issues

// Implement reconnection logicasync handleDisconnect() {  await this.reconnect({    maxAttempts: 5,    backoff: 'exponential'  });}

Message Processing Failure

async processMessage(message) {  try {    return await this.messageProcessor(message);  } catch (error) {    if (error.code === "INVALID_FORMAT") {      return this.handleInvalidFormat(message);    }    throw error;  }}
Related Resources​

Error Handling
Edit this pageLast updated on Jan 25, 2025 by Brandon Rodríguez