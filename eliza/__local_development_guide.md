# 💻 Local Development Guide
Source: https://elizaos.github.io/eliza/docs/guides/local-development/

📘 GuidesLocal DevelopmentOn this page💻 Local Development Guide
This guide covers setting up and working with Eliza in a development environment.
Prerequisites​
You can develop either in a dev container or directly on your host machine.
Requirements:​
# RequiredNode.js (v23+; not required if using the dev container)pnpm (not required if using the dev container)GitVS Code (mandatory for using the dev container or coding)Docker (mandatory for using the dev container or database development)CUDA Toolkit (optional, for GPU acceleration)
Initial Setup​
1. Repository Setup​
Clone the repository and navigate to the project directory:
# Clone the repositorygit clone https://github.com/elizaos/eliza.gitcd eliza
2. (Optional) Run Inside a Dev Container​


Open the project directory in VS Code:
code .


In the bottom-right corner, you'll see a popup:
"Reopen in Container" – Click it.

If you don't see the popup or miss it, press F1, type:
"Reopen in Container", and select it.



Wait for the container to initialize.


Open a terminal (hotkey: `Ctrl+Shift+``) and run commands from the container terminal going forward.


3. Setup dependencies​
# Install dependenciespnpm install# Install optional dependenciespnpm install --include=optional sharp
4. Environment Configuration​
Create your development environment file:
cp .env.example .env
Configure essential development variables:
# Minimum required for local developmentOPENAI_API_KEY=sk-*           # Optional, for OpenAI features
5. Local Model Setup​
For local inference without API dependencies:
# Install CUDA support for NVIDIA GPUsnpx --no node-llama-cpp source download --gpu cuda# The system will automatically download models from# Hugging Face on first run
Development Workflow​
Running the Development Server​
# Start with default characterpnpm run dev# Start with specific characterpnpm run dev --characters="characters/my-character.json"# Start with multiple characterspnpm run dev --characters="characters/char1.json,characters/char2.json"
Development Commands​
pnpm run build          # Build the projectpnpm run clean         # Clean build artifactspnpm run dev           # Start development serverpnpm run test          # Run testspnpm run test:watch    # Run tests in watch modepnpm run lint          # Lint code
Direct Client Chat UI​
# Open a terminal and Start with specific characterpnpm run dev --characters="characters/my-character.json"
# Open a 2nd terminal and start the clientpnpm start:client
NOTE: If you are using devcontainer, add --host argument to client:
pnpm start:client --host
Look for the message:
  ➜  Local:   http://localhost:5173/
Click on that link or open a browser window to that location. Once you do that you should see the chat interface connect with the system and you can start interacting with your character.
Database Development​
SQLite (Recommended for Development)​
import { SqliteDatabaseAdapter } from "@elizaos/core/adapters";import Database from "better-sqlite3";const db = new SqliteDatabaseAdapter(new Database("./dev.db"));
In-Memory Database (for Testing)​
import { SqlJsDatabaseAdapter } from "@elizaos/core/adapters";const db = new SqlJsDatabaseAdapter(new Database(":memory:"));
Schema Management​
# Create new migrationpnpm run migration:create# Run migrationspnpm run migration:up# Rollback migrationspnpm run migration:down
Testing​
Running Tests​
# Run all testspnpm test# Run specific test filepnpm test tests/specific.test.ts# Run tests with coveragepnpm test:coverage# Run database-specific testspnpm test:sqlitepnpm test:sqljs
Writing Tests​
import { runAiTest } from "@elizaos/core/test_resources";describe("Feature Test", () => {    beforeEach(async () => {        // Setup test environment    });    it("should perform expected behavior", async () => {        const result = await runAiTest({            messages: [                {                    user: "user1",                    content: { text: "test message" },                },            ],            expected: "expected response",        });        expect(result.success).toBe(true);    });});
Plugin Development​
Creating a New Plugin​
// plugins/my-plugin/src/index.tsimport { Plugin } from "@elizaos/core/types";export const myPlugin: Plugin = {    name: "my-plugin",    description: "My custom plugin",    actions: [],    evaluators: [],    providers: [],};
Custom Action Development​
// plugins/my-plugin/src/actions/myAction.tsexport const myAction: Action = {    name: "MY_ACTION",    similes: ["SIMILAR_ACTION"],    validate: async (runtime: IAgentRuntime, message: Memory) => {        return true;    },    handler: async (runtime: IAgentRuntime, message: Memory) => {        // Implementation        return true;    },    examples: [],};
Debugging​
VS Code Configuration​
Create .vscode/launch.json:
{    "version": "0.2.0",    "configurations": [        {            "type": "node",            "request": "launch",            "name": "Debug Eliza",            "skipFiles": ["<node_internals>/**"],            "program": "${workspaceFolder}/src/index.ts",            "runtimeArgs": ["-r", "ts-node/register"],            "env": {                "DEBUG": "eliza:*"            }        }    ]}
Debugging Tips​

Enable Debug Logging

# Add to your .env fileDEBUG=eliza:*

Use Debug Points

const debug = require("debug")("eliza:dev");debug("Operation details: %O", {    operation: "functionName",    params: parameters,    result: result,});

Memory Debugging

# Increase Node.js memory for developmentNODE_OPTIONS="--max-old-space-size=8192" pnpm run dev
Common Development Tasks​
1. Adding a New Character​
{    "name": "DevBot",    "description": "Development testing bot",    "modelProvider": "openai",    "settings": {        "debug": true,        "logLevel": "debug"    }}
2. Creating Custom Services​
class CustomService extends Service {    static serviceType = ServiceType.CUSTOM;    async initialize() {        // Setup code    }    async process(input: any): Promise<any> {        // Service logic    }}
3. Working with Models​
// Local model configurationconst localModel = {    modelProvider: "llamalocal",    settings: {        modelPath: "./models/llama-7b.gguf",        contextSize: 8192,    },};// Cloud model configurationconst cloudModel = {    modelProvider: "openai",    settings: {        model: "gpt-4o-mini",        temperature: 0.7,    },};
Performance Optimization​
CUDA Setup​
For NVIDIA GPU users:

Install CUDA Toolkit with cuDNN and cuBLAS
Set environment variables:

CUDA_PATH=/usr/local/cuda  # Windows: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0
Memory Management​
class MemoryManager {    private cache = new Map();    private maxSize = 1000;    async cleanup() {        if (this.cache.size > this.maxSize) {            // Implement cleanup logic        }    }}
Troubleshooting​
Common Issues​

Model Loading Issues

# Clear model cacherm -rf ./models/*# Restart with fresh download

Database Connection Issues

# Test database connectionpnpm run test:db-connection

Memory Issues

# Check memory usagenode --trace-gc index.js
Development Tools​
# Generate TypeScript documentationpnpm run docs:generate# Check for circular dependenciespnpm run madge# Analyze bundle sizepnpm run analyze
Best Practices​


Code Organization

Place custom actions in custom_actions/
Keep character files in characters/
Store test data in tests/fixtures/



Testing Strategy

Write unit tests for new features
Use integration tests for plugins
Test with multiple model providers



Git Workflow

Create feature branches
Follow conventional commits
Keep PRs focused



Additional Tools​
Character Development​
# Generate character from Twitter datanpx tweets2character# Convert documents to knowledge basenpx folder2knowledge <path/to/folder># Add knowledge to characternpx knowledge2character <character-file> <knowledge-file>
Development Scripts​
# Analyze codebase./scripts/analyze-codebase.ts# Extract tweets for training./scripts/extracttweets.js# Clean build artifacts./scripts/clean.sh
Further Resources​

Configuration Guide for setup details
Advanced Usage for complex features
API Documentation for complete API reference
Contributing Guide for contribution guidelines
Edit this pageLast updated on Jan 8, 2025 by Proteus