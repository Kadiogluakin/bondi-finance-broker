#!/bin/bash

# Setup and Run Script for Bondi Broker Agent

echo "🚀 Setting up Bondi Broker Agent..."

# Install dependencies
echo "📦 Installing dependencies..."
pnpm install

# Setup .env file if it doesn't exist
if [ ! -f .env ]; then
  echo "📝 Creating .env file..."
  cp .env.example .env
  echo "⚠️ Please edit .env file with your API keys and configuration!"
  exit 1
fi

# Check if abi files exist
if [ ! -d "../abi" ]; then
  echo "⚠️ ABI directory not found. Make sure you have the abi folder with USDC, AUSD, and funding contract ABIs."
  exit 1
fi

# Ensure we have the character file
if [ ! -f "characters/bondi_broker.character.json" ]; then
  echo "⚠️ Character file not found. Make sure characters/bondi_broker.character.json exists."
  exit 1
fi

# Start the agent
echo "🤖 Starting Bondi broker agent..."
pnpm start --character=characters/bondi_broker.character.json

echo "💬 Agent is running. You can interact with it on Telegram." 