# Quickstart Guide
Source: https://elizaos.github.io/eliza/docs/quickstart/

🏁 Getting Started⭐ Quick StartOn this pageQuickstart Guide
Prerequisites​
Before getting started with Eliza, ensure you have:

Node.js 23+ (using nvm is recommended)
pnpm 9+
Git for version control
A code editor (VS Code, Cursor or VSCodium recommended)
CUDA Toolkit (optional, for GPU acceleration)

Installation​
Clone the repository
git clone https://github.com/elizaOS/eliza.git
Enter directory
cd eliza
Switch to latest stable version tag
# This project moves quickly, check out the latest release known to workgit checkout $(git describe --tags --abbrev=0)
Install dependencies
pnpm install --no-frozen-lockfile
Note: Please only use the --no-frozen-lockfile option when you're initially instantiating the repo or are bumping the version of a package or adding a new package to your package.json. This practice helps maintain consistency in your project's dependencies and prevents unintended changes to the lockfile.
Build the local libraries
pnpm build
Configure Environment​
Copy example environment file
cp .env.example .env
Edit .env and add your values. Do NOT add this file to version control.
# Suggested quickstart environment variablesDISCORD_APPLICATION_ID=  # For Discord integrationDISCORD_API_TOKEN=      # Bot tokenHEURIST_API_KEY=       # Heurist API key for LLM and image generationOPENAI_API_KEY=        # OpenAI API keyGROK_API_KEY=          # Grok API keyELEVENLABS_XI_API_KEY= # API key from elevenlabs (for voice)LIVEPEER_GATEWAY_URL=  # Livepeer gateway URL
Choose Your Model​
Eliza supports multiple AI models and you set which model to use inside the character JSON file.


Heurist: Set modelProvider: "heurist" in your character file. Most models are uncensored.


LLM: Select available LLMs here and configure SMALL_HEURIST_MODEL,MEDIUM_HEURIST_MODEL,LARGE_HEURIST_MODEL


Image Generation: Select available Stable Diffusion or Flux models here and configure HEURIST_IMAGE_MODEL (default is FLUX.1-dev)


Llama: Set OLLAMA_MODEL to your chosen model


Grok: Set GROK_API_KEY to your Grok API key and set modelProvider: "grok" in your character file


OpenAI: Set OPENAI_API_KEY to your OpenAI API key and set modelProvider: "openai" in your character file


Livepeer: Set LIVEPEER_IMAGE_MODEL to your chosen Livepeer image model, available models here


Llama: Set XAI_MODEL=meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo


Grok: Set XAI_MODEL=grok-beta


OpenAI: Set XAI_MODEL=gpt-4o-mini or gpt-4o


Livepeer: Set SMALL_LIVEPEER_MODEL,MEDIUM_LIVEPEER_MODEL,LARGE_LIVEPEER_MODEL and IMAGE_LIVEPEER_MODEL to your desired models listed here.


Local inference​
For llama_local inference:​

The system will automatically download the model from Hugging Face
LOCAL_LLAMA_PROVIDER can be blank

Note: llama_local requires a GPU, it currently will not work with CPU inference
For Ollama inference:​

If OLLAMA_SERVER_URL is left blank, it defaults to localhost:11434
If OLLAMA_EMBEDDING_MODE is left blank, it defaults to mxbai-embed-large

Create Your First Agent​
Create a Character File
Check out the characters/ directory for a number of character files to try out.
Additionally you can read packages/core/src/defaultCharacter.ts.
Copy one of the example character files and make it your own
cp characters/sbf.character.json characters/deep-thought.character.json
📝 Character Documentation
Start the Agent
Inform it which character you want to run:
pnpm start --character="characters/deep-thought.character.json"
You can load multiple characters with a comma-separated list:
pnpm start --characters="characters/deep-thought.character.json, characters/sbf.character.json"
Interact with the Agent
Now you're ready to start a conversation with your agent.
Open a new terminal window and run the client's http server.
pnpm start:client
Once the client is running, you'll see a message like this:
➜  Local:   http://localhost:5173/
Simply click the link or open your browser to http://localhost:5173/. You'll see the chat interface connect to the system, and you can begin interacting with your character.
Platform Integration​
Discord Bot Setup​

Create a new application at Discord Developer Portal
Create a bot and get your token
Add bot to your server using OAuth2 URL generator
Set DISCORD_API_TOKEN and DISCORD_APPLICATION_ID in your .env

Twitter Integration​
Add to your .env:
TWITTER_USERNAME=  # Account usernameTWITTER_PASSWORD=  # Account passwordTWITTER_EMAIL=    # Account email
Important: Log in to the Twitter Developer Portal and enable the "Automated" label for your account to avoid being flagged as inauthentic.
Telegram Bot​

Create a bot
Add your bot token to .env:

TELEGRAM_BOT_TOKEN=your_token_here
Optional: GPU Acceleration​
If you have an NVIDIA GPU:
# Install CUDA supportnpx --no node-llama-cpp source download --gpu cuda# Ensure CUDA Toolkit, cuDNN, and cuBLAS are installed
Basic Usage Examples​
Chat with Your Agent​
# Start chat interfacepnpm start
Run Multiple Agents​
pnpm start --characters="characters/trump.character.json,characters/tate.character.json"
Common Issues & Solutions​

Node.js Version


Ensure Node.js 23.3.0 is installed
Use node -v to check version
Consider using nvm to manage Node versions

NOTE: pnpm may be bundled with a different node version, ignoring nvm. If this is the case, you can use
pnpm env use --global 23.3.0
to force it to use the correct one.

Sharp Installation
If you see Sharp-related errors:

pnpm install --include=optional sharp

CUDA Setup


Verify CUDA Toolkit installation
Check GPU compatibility with toolkit
Ensure proper environment variables are set


Exit Status 1
If you see

triggerUncaughtException(^[Object: null prototype] {[Symbol(nodejs.util.inspect.custom)]: [Function: [nodejs.util.inspect.custom]]}
You can try these steps, which aim to add @types/node to various parts of the project
# Add dependencies to workspace rootpnpm add -w -D ts-node typescript @types/node# Add dependencies to the agent package specificallypnpm add -D ts-node typescript @types/node --filter "@elizaos/agent"# Also add to the core package since it's needed there toopnpm add -D ts-node typescript @types/node --filter "@elizaos/core"# First clean everythingpnpm clean# Install all dependencies recursivelypnpm install -r# Build the projectpnpm build# Then try to startpnpm start

Better sqlite3 was compiled against a different Node.js version
If you see

Error starting agents: Error: The module '.../eliza-agents/dv/eliza/node_modules/better-sqlite3/build/Release/better_sqlite3.node'was compiled against a different Node.js version usingNODE_MODULE_VERSION 131. This version of Node.js requiresNODE_MODULE_VERSION 127. Please try re-compiling or re-installing
You can try this, which will attempt to rebuild better-sqlite3.
pnpm rebuild better-sqlite3
If that doesn't work, try clearing your node_modules in the root folder
rm -fr node_modules; pnpm store prune
Then reinstall the requirements
pnpm i
Next Steps​
Once you have your agent running, explore:

🤖 Understand Agents
📝 Create Custom Characters
⚡ Add Custom Actions
🔧 Advanced Configuration

For detailed API documentation, troubleshooting, and advanced features, check out our full documentation.
Join our Discord community for support and updates!Edit this pageLast updated on Jan 23, 2025 by Bealers