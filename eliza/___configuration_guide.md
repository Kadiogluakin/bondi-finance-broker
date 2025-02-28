# ⚙️ Configuration Guide
Source: https://elizaos.github.io/eliza/docs/guides/configuration/

📘 GuidesConfigurationOn this page⚙️ Configuration Guide
This guide covers how to configure Eliza for different use cases and environments. We'll walk through all available configuration options and best practices.
Environment Configuration​
Basic Setup​
The first step is creating your environment configuration file:
cp .env.example .env
Core Environment Variables​
Here are the essential environment variables you need to configure:
# Core API KeysOPENAI_API_KEY=sk-your-key # Required for OpenAI featuresANTHROPIC_API_KEY=your-key  # Required for Claude modelsTOGETHER_API_KEY=your-key   # Required for Together.ai models
Client-Specific Configuration​
Discord Configuration​
DISCORD_APPLICATION_ID=     # Your Discord app IDDISCORD_API_TOKEN=         # Discord bot token
Twitter Configuration​
TWITTER_USERNAME=          # Bot Twitter usernameTWITTER_PASSWORD=          # Bot Twitter passwordTWITTER_EMAIL=            # Twitter account emailTWITTER_DRY_RUN=false    # Test mode without posting
Telegram Configuration​
TELEGRAM_BOT_TOKEN=       # Telegram bot token
Model Provider Settings​
You can configure different AI model providers:
# OpenAI SettingsOPENAI_API_KEY=sk-*# Anthropic SettingsANTHROPIC_API_KEY=# Together.ai SettingsTOGETHER_API_KEY=# Heurist SettingsHEURIST_API_KEY=# Livepeer SettingsLIVEPEER_GATEWAY_URL=
Cloudflare AI Gateway Integration​
Eliza supports routing API calls through Cloudflare AI Gateway, which provides several benefits:

Detailed analytics and monitoring of message traffic and response times
Cost optimization through request caching and usage tracking across providers
Improved latency through Cloudflare's global network
Comprehensive visibility into message content and token usage
Cost analysis and comparison between different AI providers
Usage patterns and trends visualization
Request/response logging for debugging and optimization

To enable Cloudflare AI Gateway:
# Cloudflare AI Gateway SettingsCLOUDFLARE_GW_ENABLED=trueCLOUDFLARE_AI_ACCOUNT_ID=your-account-idCLOUDFLARE_AI_GATEWAY_ID=your-gateway-id
Supported providers through Cloudflare AI Gateway:

OpenAI
Anthropic
Groq

When enabled, Eliza will automatically route requests through your Cloudflare AI Gateway endpoint. The gateway URL is constructed in the format:
https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/${provider}
If the gateway configuration is incomplete or disabled, Eliza will fall back to direct API calls.
# Cloudflare AI Gateway SettingsCLOUDFLARE_GW_ENABLED=trueCLOUDFLARE_AI_ACCOUNT_ID=your-account-idCLOUDFLARE_AI_GATEWAY_ID=your-gateway-id
Supported providers through Cloudflare AI Gateway:

OpenAI
Anthropic
Groq

When enabled, Eliza will automatically route requests through your Cloudflare AI Gateway endpoint. The gateway URL is constructed in the format:
https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/${provider}
If the gateway configuration is incomplete or disabled, Eliza will fall back to direct API calls.
Image Generation​
Configure image generation in your character file:
{    "modelProvider": "heurist",    "settings": {        "imageSettings": {            "steps": 20,            "width": 1024,            "height": 1024        }    }}
Example usage:
const result = await generateImage(    {        prompt: 'A cute anime girl with big breasts and straight long black hair wearing orange T-shirt. The T-shirt has "ai16z" texts in the front. The girl is looking at the viewer',        width: 1024,        height: 1024,        numIterations: 20, // optional        guidanceScale: 3, // optional        seed: -1, // optional        modelId: "FLUX.1-dev", // optional    },    runtime,);
Character Configuration​
Character File Structure​
Character files define your agent's personality and behavior. Create them in the characters/ directory:
{    "name": "AgentName",    "clients": ["discord", "twitter"],    "modelProvider": "openai",    "settings": {        "secrets": {            "OPENAI_API_KEY": "character-specific-key",            "DISCORD_TOKEN": "bot-specific-token"        }    }}
Loading Characters​
You can load characters in several ways:
# Load default characterpnpm start# Load specific characterpnpm start --characters="characters/your-character.json"# Load multiple characterspnpm start --characters="characters/char1.json,characters/char2.json"
Secrets for Multiple Characters​
If you don't want to have secrets in your character files because you would
like to utilize source control for collaborative development on multiple
characters, then you can put all character secrets in .env by prepending
CHARACTER.NAME. before the key name and value. For example:
# C3POCHARACTER.C3PO.DISCORD_APPLICATION_ID=abcCHARACTER.C3PO.DISCORD_API_TOKEN=xyz# DOBBYCHARACTER.DOBBY.DISCORD_APPLICATION_ID=123CHARACTER.DOBBY.DISCORD_API_TOKEN=369
Custom Actions​
Adding Custom Actions​

Create a custom_actions directory
Add your action files there
Configure in elizaConfig.yaml:

actions:    - name: myCustomAction      path: ./custom_actions/myAction.ts
Action Configuration Structure​
export const myAction: Action = {    name: "MY_ACTION",    similes: ["SIMILAR_ACTION", "ALTERNATE_NAME"],    validate: async (runtime: IAgentRuntime, message: Memory) => {        // Validation logic        return true;    },    description: "Action description",    handler: async (runtime: IAgentRuntime, message: Memory) => {        // Action logic        return true;    },};
Provider Configuration​
Database Providers​
Configure different database backends:
// SQLite (Recommended for development)import { SqliteDatabaseAdapter } from "@your-org/agent-framework/adapters";const db = new SqliteDatabaseAdapter("./dev.db");// PostgreSQL (Production)import { PostgresDatabaseAdapter } from "@your-org/agent-framework/adapters";const db = new PostgresDatabaseAdapter({    host: process.env.DB_HOST,    port: parseInt(process.env.DB_PORT),    database: process.env.DB_NAME,    user: process.env.DB_USER,    password: process.env.DB_PASSWORD,});
Model Providers​
Configure model providers in your character file:
{    "modelProvider": "openai",    "settings": {        "model": "gpt-4o-mini",        "temperature": 0.7,        "maxTokens": 2000    }}
Advanced Configuration​
Runtime Settings​
Fine-tune runtime behavior:
const settings = {    // Logging    DEBUG: "eliza:*",    LOG_LEVEL: "info",    // Performance    MAX_CONCURRENT_REQUESTS: 5,    REQUEST_TIMEOUT: 30000,    // Memory    MEMORY_TTL: 3600,    MAX_MEMORY_ITEMS: 1000,};
Plugin Configuration​
Enable and configure plugins in elizaConfig.yaml:
plugins:    - name: solana      enabled: true      settings:          network: mainnet-beta          endpoint: https://api.mainnet-beta.solana.com    - name: image-generation      enabled: true      settings:          provider: dalle          size: 1024x1024
Configuration Best Practices​


Environment Segregation

Use different .env files for different environments
Follow naming convention: .env.development, .env.staging, .env.production



Secret Management

Never commit secrets to version control
Use secret management services in production
Rotate API keys regularly



Character Configuration

Keep character files modular and focused
Use inheritance for shared traits
Document character behaviors



Plugin Management

Enable only needed plugins
Configure plugin-specific settings in separate files
Monitor plugin performance



Database Configuration

Use SQLite for development
Configure connection pooling for production
Set up proper indexes



Troubleshooting​
Common Issues​


Environment Variables Not Loading
# Check .env file locationnode -e "console.log(require('path').resolve('.env'))"# Verify environment variablesnode -e "console.log(process.env)"


Character Loading Failures
# Validate character filenpx ajv validate -s character-schema.json -d your-character.json


Database Connection Issues
# Test database connectionnpx ts-node scripts/test-db-connection.ts


Configuration Validation​
Use the built-in config validator:
pnpm run validate-config
This will check:

Environment variables
Character files
Database configuration
Plugin settings

Further Resources​

Quickstart Guide for initial setup
Secrets Management for secure configuration
Local Development for development setup
Advanced Usage for complex configurations
Edit this pageLast updated on Jan 22, 2025 by Shawn Anderson