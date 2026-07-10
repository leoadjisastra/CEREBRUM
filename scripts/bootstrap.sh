#!/bin/bash
set -e
echo "Setting up CEREBRUM environment..."
cp -n .env.example .env 2>/dev/null || true
echo "Done. Edit .env with your API keys."
