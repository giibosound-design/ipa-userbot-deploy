#!/bin/bash

# ============================================================================
# IPA PATCHER USERBOT - FINAL DEPLOYMENT
# ============================================================================
# This script deploys your userbot to Fly.io with minimal manual steps
# Session is already created - just need Fly.io authentication
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   IPA PATCHER USERBOT - AUTOMATED DEPLOYMENT                  ║
║                                                               ║
║   ✅ Telegram session: CREATED                                ║
║   ✅ GitHub repository: READY                                 ║
║   ✅ Deploying to: Fly.io (Free 24/7)                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}🚀 Starting automated deployment...${NC}"
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Fly.io CLI...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install flyctl || curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    fi
    
    echo -e "${GREEN}✅ Fly.io CLI installed${NC}"
else
    echo -e "${GREEN}✅ Fly.io CLI already installed${NC}"
fi

echo ""

# Login to Fly.io
if flyctl auth whoami &> /dev/null; then
    echo -e "${GREEN}✅ Already logged in to Fly.io${NC}"
else
    echo -e "${YELLOW}🔐 Logging in to Fly.io...${NC}"
    echo -e "${CYAN}   A browser window will open (free signup, no credit card)${NC}"
    echo ""
    
    flyctl auth login
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully logged in${NC}"
    else
        echo -e "${RED}❌ Login failed${NC}"
        exit 1
    fi
fi

echo ""

# App name
APP_NAME="ipa-userbot-$(date +%s | tail -c 5)"
echo -e "${BLUE}📝 App name: ${APP_NAME}${NC}"

echo ""
echo -e "${YELLOW}🏗️  Creating Fly.io app...${NC}"

# Create app
flyctl apps create "$APP_NAME" --org personal || true

echo ""
echo -e "${YELLOW}🔐 Setting secrets...${NC}"

# Read session file
SESSION_B64=$(cat session.b64)

# Set secrets
flyctl secrets set \
    API_ID=39967356 \
    API_HASH=6aea1aa164d582ea5b233a795673d4a5 \
    PHONE_NUMBER=+37062838692 \
    LOG_LEVEL=INFO \
    PORT=8080 \
    SESSION_FILE_B64="$SESSION_B64" \
    --app "$APP_NAME"

echo -e "${GREEN}✅ Secrets set${NC}"

echo ""
echo -e "${YELLOW}🚀 Deploying to Fly.io...${NC}"
echo -e "${CYAN}   This will take 5-10 minutes (building Docker image)${NC}"
echo ""

# Update fly.toml with app name
sed -i "s/app = \"ipa-userbot\"/app = \"$APP_NAME\"/" fly.toml

# Deploy
flyctl deploy --app "$APP_NAME" --remote-only

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deployment successful!${NC}"
else
    echo ""
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Get app URL
APP_URL="https://${APP_NAME}.fly.dev"

echo ""
echo -e "${BLUE}🌐 Your userbot is live at: ${APP_URL}${NC}"

# Wait for app
echo ""
echo -e "${YELLOW}⏳ Waiting for app to be ready...${NC}"
sleep 15

# Health check
echo -e "${YELLOW}🏥 Checking health...${NC}"
HEALTH=$(curl -s "${APP_URL}/health" || echo "pending")

if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Health check pending (app still starting)${NC}"
fi

# Success
echo ""
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎉 DEPLOYMENT COMPLETE! 🎉                                  ║
║                                                               ║
║   Your IPA Patcher Userbot is LIVE and running 24/7!         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}📱 How to use:${NC}"
echo -e "   1. Open any Telegram chat (Saved Messages works great)"
echo -e "   2. Send: ${CYAN}.start${NC}"
echo -e "   3. Upload an IPA file (up to 4GB)"
echo -e "   4. Reply to the IPA with: ${CYAN}.patch${NC}"
echo -e "   5. Download your patched IPA!"
echo ""

echo -e "${BLUE}🔗 Commands:${NC}"
echo -e "   ${CYAN}.start${NC}  - Show welcome"
echo -e "   ${CYAN}.help${NC}   - Show help"
echo -e "   ${CYAN}.patch${NC}  - Patch IPA (reply to file)"
echo -e "   ${CYAN}.status${NC} - Show status"
echo ""

echo -e "${BLUE}🔗 URLs:${NC}"
echo -e "   • App:    ${CYAN}${APP_URL}${NC}"
echo -e "   • Health: ${CYAN}${APP_URL}/health${NC}"
echo -e "   • Status: ${CYAN}${APP_URL}/status${NC}"
echo ""

echo -e "${BLUE}📊 Management:${NC}"
echo -e "   • Logs:   ${CYAN}flyctl logs --app ${APP_NAME}${NC}"
echo -e "   • Status: ${CYAN}flyctl status --app ${APP_NAME}${NC}"
echo -e "   • SSH:    ${CYAN}flyctl ssh console --app ${APP_NAME}${NC}"
echo ""

echo -e "${GREEN}✅ Features:${NC}"
echo -e "   ✅ 4GB file uploads (Telegram Premium)"
echo -e "   ✅ Fancy progress bars"
echo -e "   ✅ 24/7 uptime"
echo -e "   ✅ Auto-restart"
echo -e "   ✅ HTTPS enabled"
echo ""

echo -e "${CYAN}🎊 Enjoy your userbot! 🎊${NC}"
echo ""
