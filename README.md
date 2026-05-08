# 🔥 Valakas VPS Bot

A fully professional Discord VPS control bot — everything named **Valakas**.

---

## ⚡ Quick Install (VPS)

```bash
git clone https://github.com/YOURNAME/valakas
cd valakas
chmod +x install.valakas
bash install.valakas
```

---

## 🐳 Docker Install

```bash
# Build
docker build -t valakas-bot .

# Run (replace YOUR_TOKEN and YOUR_ID)
docker run -d \
  --name valakas \
  --restart always \
  -e TOKEN=YOUR_BOT_TOKEN \
  valakas-bot
```

---

## 📋 Commands

| Command | Description |
|---|---|
| `!help` | Show all commands |
| `!stats` | Full VPS stats |
| `!cpu` | CPU usage |
| `!ram` | RAM usage |
| `!disk` | Disk usage |
| `!uptime` | Bot & VPS uptime |
| `!ping` | Bot latency |
| `!ip` | Server public IP |
| `!ps` | Top processes |
| `!run <cmd>` | Run shell command |
| `!restart` | Restart bot |
| `!reboot` | Reboot VPS |
| `!update` | apt update & upgrade |
| `!install <pkg>` | Install package |
| `!kill <pid>` | Kill a process |
| `!dps` | Docker containers |
| `!dstart <name>` | Start container |
| `!dstop <name>` | Stop container |
| `!drestart <name>` | Restart container |
| `!dlogs <name>` | Container logs |
| `!ls [path]` | List files |
| `!cat <file>` | Read file |
| `!mkdir <dir>` | Make directory |
| `!rm <file>` | Delete file |
| `!ports` | Open ports |
| `!netstat` | Network stats |
| `!speedtest` | Run speedtest |

---

## ⚙️ Setup

1. Go to [discord.dev](https://discord.com/developers/applications)
2. Create a new application → name it **Valakas**
3. Bot section → copy your token
4. Enable all **Privileged Gateway Intents**
5. Invite bot with `Administrator` permission
6. Edit `valakas.py`:
   - Set `TOKEN = "your_token"`
   - Set `OWNER_IDS = [your_discord_id]`

---

**Made with 🔥 — Valakas VPS Bot**
