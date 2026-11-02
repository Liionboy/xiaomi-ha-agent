#!/bin/bash
# Startup script for Xiaomi Home Assistant Agent

set -e

echo "🚀 Starting Xiaomi Home Assistant Agent..."
echo "=========================================="

# Start the application
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8099 --workers 1
