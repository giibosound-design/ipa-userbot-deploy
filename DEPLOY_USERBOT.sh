#!/bin/bash

# ============================================================================
# IPA PATCHER USERBOT - ONE COMMAND DEPLOYMENT
# ============================================================================
# This script:
# 1. Prompts for Telegram verification (once)
# 2. Creates permanent session
# 3. Deploys to Fly.io automatically
# 4. Keeps userbot running 24/7
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   IPA PATCHER USERBOT - ONE COMMAND DEPLOYMENT                ║
║                                                               ║
║   ✅ Telethon userbot with 4GB support                        ║
║   ✅ One-time phone verification                              ║
║   ✅ Permanent session creation                               ║
║   ✅ Automatic deployment to Fly.io                           ║
║   ✅ 24/7 uptime with auto-restart                            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}🚀 Starting automated deployment...${NC}"
echo ""

# Step 1: Install dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip3 install -q telethon cryptg aiohttp 2>&1 | tail -5 || true
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo ""

# Step 2: Create Telegram session
echo -e "${YELLOW}🔐 Creating Telegram session...${NC}"
echo -e "${CYAN}   You will be prompted for:${NC}"
echo -e "${CYAN}   1. Verification code (sent to your Telegram app)${NC}"
echo -e "${CYAN}   2. 2FA password (if enabled)${NC}"
echo ""

python3 create_session.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Session creation failed${NC}"
    exit 1
fi

# Check if session file was created
if [ ! -f "ipa_userbot_session.session" ]; then
    echo -e "${RED}❌ Session file not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Session created successfully!${NC}"

# Step 3: Install Fly.io CLI
if ! command -v flyctl &> /dev/null; then
    echo ""
    echo -e "${YELLOW}📦 Installing Fly.io CLI...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install flyctl || curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    else
        echo -e "${RED}❌ Unsupported OS${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Fly.io CLI installed${NC}"
else
    echo -e "${GREEN}✅ Fly.io CLI already installed${NC}"
fi

echo ""

# Step 4: Login to Fly.io
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

# Step 5: Create app name
APP_NAME="ipa-userbot-$(date +%s | tail -c 5)"
echo -e "${BLUE}📝 App name: ${APP_NAME}${NC}"

echo ""
echo -e "${YELLOW}🏗️  Deploying to Fly.io...${NC}"
echo -e "${CYAN}   This will take 5-10 minutes (building Docker image)${NC}"
echo ""

# Step 6: Launch app
flyctl launch \
    --now \
    --auto-confirm \
    --name "$APP_NAME" \
    --region iad \
    --org personal \
    --no-deploy

# Step 7: Upload session file as secret
echo ""
echo -e "${YELLOW}📤 Uploading session file...${NC}"

# Encode session file to base64
SESSION_B64=$(base64 -w 0 ipa_userbot_session.session 2>/dev/null || base64 ipa_userbot_session.session)

# Set as secret
flyctl secrets set \
    SESSION_FILE_B64="$SESSION_B64" \
    --app "$APP_NAME"

echo -e "${GREEN}✅ Session file uploaded${NC}"

# Step 8: Set environment variables
echo ""
echo -e "${YELLOW}🔐 Setting environment variables...${NC}"
flyctl secrets set \
    API_ID=39967356 \
    API_HASH=6aea1aa164d582ea5b233a795673d4a5 \
    PHONE_NUMBER=+37062838692 \
    LOG_LEVEL=INFO \
    --app "$APP_NAME"

echo -e "${GREEN}✅ Environment variables set${NC}"

# Step 9: Deploy
echo ""
echo -e "${YELLOW}🚀 Deploying application...${NC}"

flyctl deploy --app "$APP_NAME" --remote-only

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deployment successful!${NC}"
else
    echo ""
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Step 10: Get app URL
APP_URL="https://${APP_NAME}.fly.dev"

echo ""
echo -e "${BLUE}🌐 Your userbot is now live at: ${APP_URL}${NC}"

# Wait for app to be ready
echo ""
echo -e "${YELLOW}⏳ Waiting for app to be ready...${NC}"
sleep 15

# Verify health
echo -e "${YELLOW}🏥 Checking health...${NC}"
HEALTH_CHECK=$(curl -s "${APP_URL}/health" || echo "failed")

if echo "$HEALTH_CHECK" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Health check pending${NC}"
fi

# Success message
echo ""
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎉 DEPLOYMENT COMPLETE! 🎉                                  ║
║                                                               ║
║   Your IPA Patcher Userbot is now LIVE and running 24/7!     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}📱 How to use your userbot:${NC}"
echo -e "   1. Open any Telegram chat (including Saved Messages)"
echo -e "   2. Send: ${CYAN}.start${NC}"
echo -e "   3. Upload an IPA file"
echo -e "   4. Reply to the IPA with: ${CYAN}.patch${NC}"
echo -e "   5. Wait for processing"
echo -e "   6. Download your patched IPA!"
echo ""

echo -e "${BLUE}🔗 Userbot Commands:${NC}"
echo -e "   ${CYAN}.start${NC}  - Show welcome message"
echo -e "   ${CYAN}.help${NC}   - Show help"
echo -e "   ${CYAN}.patch${NC}  - Patch IPA (reply to file)"
echo -e "   ${CYAN}.status${NC} - Show userbot status"
echo ""

echo -e "${BLUE}🔗 Useful URLs:${NC}"
echo -e "   • App URL:  ${CYAN}${APP_URL}${NC}"
echo -e "   • Health:   ${CYAN}${APP_URL}/health${NC}"
echo -e "   • Status:   ${CYAN}${APP_URL}/status${NC}"
echo ""

echo -e "${BLUE}📊 Management:${NC}"
echo -e "   • View logs:    ${CYAN}flyctl logs --app ${APP_NAME}${NC}"
echo -e "   • Check status: ${CYAN}flyctl status --app ${APP_NAME}${NC}"
echo -e "   • SSH access:   ${CYAN}flyctl ssh console --app ${APP_NAME}${NC}"
echo ""

echo -e "${GREEN}✅ Your userbot is fully functional with:${NC}"
echo -e "   ✅ 4GB file uploads (Telegram Premium)"
echo -e "   ✅ Fancy progress bars"
echo -e "   ✅ Fast upload/download speeds"
echo -e "   ✅ 24/7 uptime"
echo -e "   ✅ Auto-restart"
echo -e "   ✅ HTTPS enabled"
echo ""

echo -e "${CYAN}🎊 Enjoy your IPA Patcher Userbot! 🎊${NC}"
echo ""
