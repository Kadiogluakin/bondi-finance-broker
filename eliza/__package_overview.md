# 📖 Package Overview
Source: https://elizaos.github.io/eliza/docs/packages/

📦 PackagesOverviewOn this page📖 Package Overview
Core Components​

@elizaos/core: Central framework and shared functionality
@elizaos/agent: Agent runtime and management
@elizaos/adapters: Database implementations (PostgreSQL, SQLite, etc.)
@elizaos/clients: Platform integrations (Discord, Telegram, etc.)
@elizaos/plugins: Extension modules for additional functionality

Package Architecture​
The Eliza framework is built on a modular architecture where each package serves a specific purpose:

Core Package: Provides the fundamental building blocks
Agent Package: Handles agent lifecycle and runtime
Adapters: Enable different storage backends
Clients: Connect to various platforms
Plugins: Add specialized capabilities

Package Dependencies​

Getting Started​
# Install core packagepnpm add @elizaos/core# Install specific adapterspnpm add @elizaos/adapter-postgrespnpm add @elizaos/adapter-sqlite# Install clientspnpm add @elizaos/client-discordpnpm add @elizaos/client-TelegramEdit this pageLast updated on Dec 22, 2024 by Shaw