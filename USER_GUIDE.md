# 🤖 IPA Patcher Bot - User Guide

## ✅ Your Bot is Live and Ready!

**App URL:** https://ipa-userbot-6355.fly.dev/  
**Status:** ✅ ONLINE  
**Account:** @ywtmsh  

---

## 📱 How to Use

### Step 1: Start the Bot

Open any Telegram chat (Saved Messages recommended) and send:

```
/start
```

You'll see a menu with buttons:
- 🔧 **Patch IPA** - Patch uploaded IPA files
- 📊 **Bot Status** - Check bot status
- ℹ️ **Help** - Show help
- 🗑️ **Clear Files** - Remove uploaded files

---

### Step 2: Upload an IPA File

Simply upload an IPA file to the chat (up to 4GB with Telegram Premium).

The bot will:
- ✅ Download the file automatically
- ✅ Show download progress
- ✅ Display file size
- ✅ Show "Patch IPA" button

---

### Step 3: Patch the IPA

Click the **"🔧 Patch IPA"** button.

The bot will:
1. ⏳ Start patching process
2. 🔧 Inject blatantsPatch.dylib
3. 📤 Upload patched IPA
4. ✅ Send you the patched file

---

## 🎮 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu with buttons |
| `/help` | Show detailed help |
| `/status` | Show bot and account status |
| `/clear` | Clear all uploaded files |

---

## ✨ Features

### 4GB File Support
✅ Full Telegram Premium support  
✅ Upload files up to 4GB  
✅ Fast upload/download speeds  

### Progress Bars
✅ Real-time download progress  
✅ Real-time upload progress  
✅ File size display  

### IPA Patching
✅ Automatic dylib injection  
✅ blatantsPatch.dylib included  
✅ Works with all IPA files  

### User Interface
✅ Inline keyboard buttons  
✅ Clean, professional design  
✅ Easy navigation  
✅ Error messages with retry options  

---

## 📊 Example Workflow

1. **Send `/start`** to open the menu
2. **Upload** an IPA file (e.g., `MyApp.ipa`)
3. Bot downloads and shows: "✅ Download complete!"
4. **Click** "🔧 Patch IPA" button
5. Bot patches and uploads: "✅ IPA Patched Successfully!"
6. **Download** your patched IPA
7. **Install** on your device

---

## 🔧 Supported Files

| Extension | Description | Supported |
|-----------|-------------|-----------|
| `.ipa` | iOS Application | ✅ Yes |
| `.deb` | Debian Package | ✅ Yes |
| `.dylib` | Dynamic Library | ✅ Yes |

---

## 🆘 Troubleshooting

### Bot Not Responding?

**Check if bot is running:**
```bash
curl https://ipa-userbot-6355.fly.dev/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "userbot": "running",
  "type": "telethon"
}
```

**If not healthy, restart:**
```bash
flyctl apps restart ipa-userbot-6355
```

---

### Commands Not Working?

Make sure:
- ✅ You're using `/` prefix (not `.`)
- ✅ You're logged in as @ywtmsh
- ✅ Bot is running (check health)
- ✅ You have internet connection

---

### File Upload Fails?

**Check:**
- File size (max 4GB with Premium, 2GB without)
- File type (.ipa, .deb, .dylib)
- Internet connection
- Telegram app is updated

**Try:**
- Upload to Saved Messages first
- Compress the file if too large
- Check file isn't corrupted

---

### Patching Fails?

**Common causes:**
- Invalid IPA file
- Corrupted download
- Insufficient disk space
- IPA already patched

**Solutions:**
- Try a different IPA
- Re-upload the file
- Use `/clear` to free space
- Check IPA file integrity

---

## 🔐 Security & Privacy

### Your Data
- ✅ Files are processed temporarily
- ✅ Automatic cleanup after processing
- ✅ No data stored permanently
- ✅ Secure HTTPS connections

### Session Security
- ✅ Session encrypted on Fly.io
- ✅ Only accessible by you
- ✅ Can be revoked anytime
- ✅ 2FA recommended

### Revoking Access
If you want to revoke the bot's access:
1. Open Telegram Settings
2. Go to Privacy & Security → Devices
3. Find the session and terminate it

---

## 💰 Cost

- **Fly.io Hosting:** ~$1-2/month
- **Telegram API:** Free
- **SSL/HTTPS:** Free (included)
- **Bandwidth:** Included

**Total:** ~$1-2/month

---

## 📈 Monitoring

### Health Check
```bash
curl https://ipa-userbot-6355.fly.dev/health
```

### Status Check
```bash
curl https://ipa-userbot-6355.fly.dev/status
```

### View Logs
```bash
flyctl logs --app ipa-userbot-6355
```

### Dashboard
https://fly.io/apps/ipa-userbot-6355/monitoring

---

## 🎯 Tips & Tricks

### Faster Processing
- Use Saved Messages for testing
- Upload files during off-peak hours
- Keep files under 1GB for faster processing

### Best Practices
- Clear files regularly with `/clear`
- Check `/status` before large uploads
- Use `/help` if unsure about features

### Optimization
- Telegram Premium = 4GB support
- Fast internet = faster uploads
- Smaller files = quicker patching

---

## 📞 Quick Reference

**Commands:**
- `/start` - Main menu
- `/help` - Help
- `/status` - Status
- `/clear` - Clear files

**URLs:**
- App: https://ipa-userbot-6355.fly.dev/
- Health: https://ipa-userbot-6355.fly.dev/health
- Status: https://ipa-userbot-6355.fly.dev/status
- GitHub: https://github.com/giibosound-design/ipa-userbot-deploy

**Account:**
- Username: @ywtmsh
- Premium: Yes ✅
- 4GB Support: Enabled ✅

---

## 🎊 Enjoy Your Bot!

Your IPA Patcher Bot is:
- ✅ Running 24/7
- ✅ Fully functional
- ✅ Ready to use
- ✅ Automatically maintained

**Just send `/start` in Telegram and start patching!** 🚀

---

**Need help?** Check the logs or restart the bot.  
**Having issues?** See the Troubleshooting section above.  
**Want to contribute?** Fork the GitHub repo!  

🎉 **Happy Patching!** 🎉
