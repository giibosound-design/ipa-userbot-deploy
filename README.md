# IPA Patcher Userbot - Telethon Edition

A **Telethon-based userbot** that runs as your Telegram account with full 4GB file support, fancy progress bars, and automatic IPA patching.

## 🚀 ONE COMMAND DEPLOYMENT

```bash
./DEPLOY_USERBOT.sh
```

That's it! The script will:

1. ✅ Prompt for Telegram verification (one time only)
2. ✅ Create permanent session file
3. ✅ Deploy to Fly.io automatically
4. ✅ Keep userbot running 24/7

**Time**: 5-10 minutes  
**Cost**: $0/month forever  
**Manual input**: Only Telegram verification code

---

## ✨ Features

### Full Telegram Premium Support
- ✅ **4GB file uploads/downloads**
- ✅ **Fast upload/download speeds**
- ✅ **Fancy progress bars**
- ✅ **No file size limits** (up to Telegram's 4GB limit)

### Userbot Capabilities
- ✅ **Runs as your account** (not a bot)
- ✅ **Works in any chat** (including Saved Messages)
- ✅ **Command-based** (`.patch`, `.start`, etc.)
- ✅ **Automatic IPA patching**
- ✅ **Session persistence**

### Infrastructure
- ✅ **24/7 uptime** on Fly.io
- ✅ **Auto-restart** on failures
- ✅ **Health monitoring**
- ✅ **HTTPS enabled**
- ✅ **Free hosting**

---

## 📋 Requirements

- **Telegram account** (phone: +37062838692)
- **Telegram Premium** (for 4GB support)
- **Linux/macOS** (or Windows WSL)
- **Internet connection**

---

## 🎯 How to Use

### After Deployment

1. **Open any Telegram chat** (Saved Messages recommended)
2. **Send**: `.start`
3. **Upload an IPA file** (up to 4GB)
4. **Reply to the IPA** with: `.patch`
5. **Wait** for processing (progress bar will show)
6. **Download** your patched IPA!

### Commands

- `.start` - Show welcome message
- `.help` - Show help and commands
- `.patch` - Patch IPA file (reply to file)
- `.status` - Show userbot status

---

## 🔧 Deployment Details

### What the Script Does

1. **Installs dependencies** (Telethon, cryptg, aiohttp)
2. **Creates session**:
   - Prompts for phone number (+37062838692)
   - Sends verification code to your Telegram
   - You enter the code
   - Creates permanent session file
3. **Installs Fly.io CLI** (if needed)
4. **Logs in to Fly.io** (browser popup, free signup)
5. **Uploads session** to Fly.io as encrypted secret
6. **Deploys userbot** to Fly.io
7. **Starts 24/7 operation**

### Session Security

- Session file is **encrypted** and stored securely
- Uploaded to Fly.io as a **secret** (not in code)
- **Never expires** (permanent session)
- **Survives restarts** (persistent)

---

## 📊 Technical Details

### Architecture

```
Telethon Userbot (runs as your account)
    ↓
Telegram MTProto API (direct connection)
    ↓
Full 4GB file support + Premium speeds
    ↓
IPA Patching with ipapatch + blatantsPatch.dylib
    ↓
Send patched IPA back to you
```

### vs Bot Token Approach

| Feature | Userbot (Telethon) | Bot Token (Pyrogram) |
|---------|-------------------|----------------------|
| File size | 4GB (Premium) | 2GB (standard) |
| Speed | Premium speeds | Standard speeds |
| Works in | Any chat | Bot chats only |
| Commands | `.command` | `/command` |
| Authentication | Phone + code | Bot token |
| Session | Permanent | Token-based |

---

## 🆘 Troubleshooting

### Session creation fails

**Check:**
- Phone number is correct (+37062838692)
- You received the verification code in Telegram
- 2FA password is correct (if enabled)

**Fix:**
```bash
# Delete old session and try again
rm -f ipa_userbot_session.session*
python3 create_session.py
```

### Deployment fails

**Check logs:**
```bash
flyctl logs --app ipa-userbot-XXXXX
```

**Common issues:**
- Session file not uploaded → Re-run deployment
- Docker build timeout → Retry deployment
- Port binding issue → Check fly.toml

### Userbot not responding

**Check if running:**
```bash
flyctl status --app ipa-userbot-XXXXX
```

**Restart:**
```bash
flyctl apps restart ipa-userbot-XXXXX
```

**View logs:**
```bash
flyctl logs --app ipa-userbot-XXXXX
```

### Commands not working

**Make sure:**
- You're using `.` prefix (not `/`)
- You're sending from the same account
- Userbot is running (check logs)

**Test:**
```
.start
```

---

## 🔐 Security Notes

- **Session file** is encrypted and stored securely
- **Never share** your session file
- **2FA recommended** for extra security
- **Session** can be revoked from Telegram settings
- **Userbot** only responds to your commands

---

## 📈 Management

### View Logs
```bash
flyctl logs --app ipa-userbot-XXXXX
```

### Check Status
```bash
flyctl status --app ipa-userbot-XXXXX
```

### SSH into Container
```bash
flyctl ssh console --app ipa-userbot-XXXXX
```

### Restart Userbot
```bash
flyctl apps restart ipa-userbot-XXXXX
```

### Stop Userbot
```bash
flyctl apps stop ipa-userbot-XXXXX
```

### Delete Userbot
```bash
flyctl apps destroy ipa-userbot-XXXXX
```

---

## 💰 Cost Breakdown

- **Fly.io hosting**: $0/month (free tier)
- **Telegram API**: $0/month (free)
- **Domain/SSL**: $0/month (included)
- **Bandwidth**: $0/month (160GB free)

**Total**: **$0/month forever**

---

## 🎁 What You Get

✅ **Fully automated deployment**  
✅ **One-time phone verification**  
✅ **Permanent session** (never expires)  
✅ **4GB file support** (with Premium)  
✅ **Fancy progress bars**  
✅ **24/7 uptime**  
✅ **Auto-restart**  
✅ **Free hosting**  
✅ **HTTPS enabled**  
✅ **Health monitoring**  

---

## 📞 Quick Reference

**Phone**: +37062838692  
**API ID**: 39967356  
**API Hash**: 6aea1aa164d582ea5b233a795673d4a5  

**Commands**:
- `.start` - Welcome
- `.help` - Help
- `.patch` - Patch IPA
- `.status` - Status

**Deployment**: `./DEPLOY_USERBOT.sh`

---

## 🎉 Success Indicators

After deployment, you should see:

✅ Session created successfully  
✅ Logged in as [Your Name]  
✅ Premium: Yes (for 4GB support)  
✅ Deployment successful  
✅ Health check passed  
✅ Userbot responds to `.start`  
✅ File upload works with progress bar  
✅ Patching completes successfully  

---

## 🚀 Next Steps

1. Run: `./DEPLOY_USERBOT.sh`
2. Enter verification code when prompted
3. Wait for deployment (5-10 minutes)
4. Send `.start` in any Telegram chat
5. Upload IPA and reply with `.patch`
6. Enjoy! 🎊

---

**Total setup time**: 5-10 minutes  
**Manual input**: Only verification code  
**Everything else**: Fully automated  

🎊 **Your userbot is ready to deploy!** 🎊
