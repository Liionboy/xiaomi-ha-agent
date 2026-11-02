#!/bin/bash
# Build and test the add-on

set -e

echo "🔨 Building Xiaomi HA Agent Add-on..."
echo "===================================="

# Change to addon directory
cd "$(dirname "$0")/addon"

# Build Docker image
echo "📦 Building Docker image..."
docker build -t xiaomi-ha-agent:latest .

echo "✅ Build complete!"
echo ""
echo "🚀 To run locally for testing:"
echo "   docker run -p 8099:8099 -e XIAOMI_API_KEY=your_key_here xiaomi-ha-agent:latest"
echo ""
echo "📦 To install in Home Assistant:"
echo "   1. Copy this folder to /addons/xiaomi_ha_agent/"
echo "   2. Install via Supervisor UI"
