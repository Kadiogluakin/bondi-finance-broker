# GitHub
Source: https://github.com/elizaos/eliza

Eliza 🤖




📑 Technical Report |  📖 Documentation | 🎯 Examples

🌍 README Translations
中文说明 | 日本語の説明 | 한국어 설명 | Persian | Français | Português | Türkçe | Русский | Español | Italiano | ไทย | Deutsch | Tiếng Việt | עִברִית | Tagalog | Polski | Arabic | Hungarian | Srpski | Română | Nederlands | Ελληνικά
🚩 Overview



✨ Features

🛠️ Full-featured Discord, X (Twitter) and Telegram connectors
🔗 Support for every model (Llama, Grok, OpenAI, Anthropic, Gemini, etc.)
👥 Multi-agent and room support
📚 Easily ingest and interact with your documents
💾 Retrievable memory and document store
🚀 Highly extensible - create your own actions and clients
📦 Just works!

Video Tutorials
AI Agent Dev School
🎯 Use Cases

🤖 Chatbots
🕵️ Autonomous Agents
📈 Business Process Handling
🎮 Video Game NPCs
🧠 Trading

🚀 Quick Start
Prerequisites

Python 2.7+
Node.js 23+
pnpm


Note for Windows Users: WSL 2 is required.

Use the Starter (Recommended)
git clone https://github.com/elizaos/eliza-starter.git
cd eliza-starter
cp .env.example .env
pnpm i && pnpm build && pnpm start
Manually Start Eliza (Only recommended if you know what you are doing)
Checkout the latest release
# Clone the repository
git clone https://github.com/elizaos/eliza.git

# This project iterates fast, so we recommend checking out the latest release
git checkout $(git describe --tags --abbrev=0)
# If the above doesn't checkout the latest release, this should work:
# git checkout $(git describe --tags `git rev-list --tags --max-count=1`)
Edit the .env file
Copy .env.example to .env and fill in the appropriate values.
cp .env.example .env

Note: .env is optional. If you're planning to run multiple distinct agents, you can pass secrets through the character JSON
Start Eliza
pnpm i
pnpm build
pnpm start

# The project iterates fast, sometimes you need to clean the project if you are coming back to the project
pnpm clean
Interact via Browser
Once the agent is running, you should see the message to run "pnpm start:client" at the end.
Open another terminal, move to the same directory, run the command below, then follow the URL to chat with your agent.
pnpm start:client
Then read the Documentation to learn how to customize your Eliza.

Automatically Start Eliza
The start script provides an automated way to set up and run Eliza:
sh scripts/start.sh
For detailed instructions on using the start script, including character management and troubleshooting, see our Start Script Guide.

Note: The start script handles all dependencies, environment setup, and character management automatically.


Modify Character


Open packages/core/src/defaultCharacter.ts to modify the default character. Uncomment and edit.


To load custom characters:

Use pnpm start --characters="path/to/your/character.json"
Multiple character files can be loaded simultaneously



Connect with X (Twitter)

change "clients": [] to "clients": ["twitter"] in the character file to connect with X




Additional Requirements
You may need to install Sharp. If you see an error when starting up, try installing it with the following command:
pnpm install --include=optional sharp


Start Eliza with Gitpod


Deploy Eliza in one click
Use Fleek to deploy Eliza in one click. This opens Eliza to non-developers and provides the following options to build your agent:

Start with a template
Build characterfile from scratch
Upload pre-made characterfile

Click here to get started!

Community & contact

GitHub Issues. Best for: bugs you encounter using Eliza, and feature proposals.
Discord. Best for: sharing your applications and hanging out with the community.

Citation
We now have a paper you can cite for the Eliza OS:
@article{walters2025eliza,
  title={Eliza: A Web3 friendly AI Agent Operating System},
  author={Walters, Shaw and Gao, Sam and Nerd, Shakker and Da, Feng and Williams, Warren and Meng, Ting-Chien and Han, Hunter and He, Frank and Zhang, Allen and Wu, Ming and others},
  journal={arXiv preprint arXiv:2501.06781},
  year={2025}
}
Contributors



Star History

