#!/bin/bash

# Deploy to Railway.app
# Railway offers $5/month free credit (enough for 24/7 uptime)

echo "======================================================================"
echo "DEPLOYING TO RAILWAY.APP"
echo "======================================================================"
echo ""

# Install Railway CLI
echo "Installing Railway CLI..."
npm install -g @railway/cli 2>&1 | tail -3

echo "✓ Railway CLI installed"
echo ""

# Check if Railway token exists
if [ -z "$RAILWAY_TOKEN" ]; then
    echo "Please login to Railway..."
    echo "A browser window will open for authentication."
    echo ""
    railway login
else
    echo "Using existing Railway token..."
fi

echo ""
echo "Creating new Railway project..."

# Initialize Railway project
railway init --name "ipa-userbot-$(date +%s)"

echo ""
echo "Setting environment variables..."

# Set environment variables
railway variables set API_ID=39967356
railway variables set API_HASH=6aea1aa164d582ea5b233a795673d4a5
railway variables set PHONE_NUMBER=+37062838692
railway variables set LOG_LEVEL=INFO
railway variables set PORT=8080
railway variables set SESSION_FILE_B64="$(cat session.b64)"

echo "✓ Environment variables set"
echo ""

echo "Deploying to Railway..."
railway up

echo ""
echo "======================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================================================================"
echo ""
echo "Getting service URL..."
railway domain

echo ""
echo "Your userbot is now deploying!"
echo "Check status: railway status"
echo "View logs: railway logs"
echo ""
echo "======================================================================"
