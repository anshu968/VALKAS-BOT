import discord
from discord.ext import commands, tasks
import subprocess
import psutil
import platform
import time
import os
import sys
import datetime
import asyncio

# ============================================================
#   VALAKAS BOT - VPS CONTROL BOT
#   Made by: RAJVEER | Bot: Valakas
# ============================================================

TOKEN = "YOUR_BOT_TOKEN_HERE"
PREFIX = "!"
OWNER_IDS = [123456789]  # Add your Discord user ID here

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

START_TIME = time.time()

# ─────────────────────────────────────────────────────────────
# EMBEDS HELPER
# ─────────────────────────────────────────────────────────────

def valakas_embed(title, description=None, color=0xFF4500):
    embed = discord.Embed(
        title=f"🔥 {title}",
        description=description,
        color=color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Valakas VPS Bot", icon_url="https://i.imgur.com/valakas.png")
    return embed

def error_embed(msg):
    return valakas_embed("❌ Error", msg, color=0xFF0000)

def success_embed(msg):
    return valakas_embed("✅ Success", msg, color=0x00FF88)

# ─────────────────────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"""
╔══════════════════════════════════════╗
║         VALAKAS BOT ONLINE           ║
║   Logged in as: {bot.user.name:<20} ║
║   ID: {bot.user.id:<30} ║
╚══════════════════════════════════════╝
    """)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Valakas VPS 🔥"
        ),
        status=discord.Status.online
    )
    update_status.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(embed=error_embed("❌ Only the **Valakas owner** can use this command!"))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_embed(f"Missing argument: `{error.param.name}`"))
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=error_embed("Unknown command! Type `!help` to see all Valakas commands."))
    else:
        await ctx.send(embed=error_embed(str(error)))

# ─────────────────────────────────────────────────────────────
# OWNER CHECK
# ─────────────────────────────────────────────────────────────

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNER_IDS
    return commands.check(predicate)

# ─────────────────────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────────────────────

@tasks.loop(minutes=5)
async def update_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"CPU:{cpu}% RAM:{ram}% 🔥"
        )
    )

# ─────────────────────────────────────────────────────────────
# HELP COMMAND
# ─────────────────────────────────────────────────────────────

@bot.command(name="help")
async def help_cmd(ctx):
    embed = valakas_embed("🔥 Valakas VPS Bot — Command List")
    embed.description = (
        "```yaml\n"
        "Prefix: !  |  Bot: Valakas  |  Owner-only commands marked with 🔒\n"
        "```"
    )

    embed.add_field(name="━━━━━━━━ 📊 STATS ━━━━━━━━", value="\u200b", inline=False)
    embed.add_field(name="", value=(
        "`!stats`  ➜  Show full VPS stats (CPU, RAM, Disk, Network, Uptime)\n"
        "`!cpu`    ➜  Show CPU usage % with visual bar\n"
        "`!ram`    ➜  Show RAM & Swap usage with visual bar\n"
        "`!disk`   ➜  Show Disk usage with visual bar\n"
        "`!uptime` ➜  Show Bot uptime and VPS uptime\n"
        "`!ip`     ➜  Show the public IP of the VPS server\n"
        "`!ping`   ➜  Show bot latency in milliseconds"
    ), inline=False)

    embed.add_field(name="━━━━━━━━ ⚙️ CONTROL 🔒 ━━━━━━━━", value="\u200b", inline=False)
    embed.add_field(name="", value=(
        "`!run <command>`   ➜  Run any shell command on the VPS\n"
        "`!ps`              ➜  Show top 10 processes by CPU usage\n"
        "`!kill <pid>`      ➜  Kill a running process by its PID\n"
        "`!install <pkg>`   ➜  Install a package using apt (e.g. !install htop)\n"
        "`!update`          ➜  Run apt update & apt upgrade on the VPS\n"
        "`!restart`         ➜  Restart the Valakas bot process\n"
        "`!reboot`          ➜  Fully reboot the VPS server"
    ), inline=False)

    embed.add_field(name="━━━━━━━━ 🐳 DOCKER 🔒 ━━━━━━━━", value="\u200b", inline=False)
    embed.add_field(name="", value=(
        "`!dps`              ➜  List all Docker containers and their status\n"
        "`!dstart <name>`    ➜  Start a stopped Docker container\n"
        "`!dstop <name>`     ➜  Stop a running Docker container\n"
        "`!drestart <name>`  ➜  Restart a Docker container\n"
        "`!dlogs <name>`     ➜  Show last 30 lines of a container's logs"
    ), inline=False)

    embed.add_field(name="━━━━━━━━ 📁 FILES 🔒 ━━━━━━━━", value="\u200b", inline=False)
    embed.add_field(name="", value=(
        "`!ls [path]`   ➜  List files in a directory (default: current folder)\n"
        "`!cat <file>`  ➜  Read and display the contents of a file\n"
        "`!mkdir <dir>` ➜  Create a new directory on the VPS\n"
        "`!rm <file>`   ➜  Delete a file or folder (use with caution!)"
    ), inline=False)

    embed.add_field(name="━━━━━━━━ 🌐 NETWORK 🔒 ━━━━━━━━", value="\u200b", inline=False)
    embed.add_field(name="", value=(
        "`!ports`      ➜  Show all open/listening ports on the VPS\n"
        "`!netstat`    ➜  Show total network sent/received stats\n"
        "`!speedtest`  ➜  Run a full internet speed test on the VPS"
    ), inline=False)

    embed.set_footer(text="Valakas VPS Bot  •  🔒 = Owner only commands")
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────────────────────
# STATS COMMANDS
# ─────────────────────────────────────────────────────────────

@bot.command(name="stats")
async def stats(ctx):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    uptime_seconds = time.time() - START_TIME
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    vps_uptime = datetime.datetime.now() - boot_time

    embed = valakas_embed("🖥️ Valakas VPS Stats")
    embed.add_field(name="🖥️ System", value=(
        f"**OS:** {platform.system()} {platform.release()}\n"
        f"**Hostname:** {platform.node()}\n"
        f"**Arch:** {platform.machine()}\n"
        f"**Python:** {platform.python_version()}"
    ), inline=True)
    embed.add_field(name="📊 Resources", value=(
        f"**CPU:** {cpu}%\n"
        f"**RAM:** {ram.percent}% ({ram.used//1024//1024}MB / {ram.total//1024//1024}MB)\n"
        f"**Disk:** {disk.percent}% ({disk.used//1024//1024//1024}GB / {disk.total//1024//1024//1024}GB)"
    ), inline=True)
    embed.add_field(name="🌐 Network", value=(
        f"**Sent:** {net.bytes_sent//1024//1024}MB\n"
        f"**Recv:** {net.bytes_recv//1024//1024}MB"
    ), inline=True)
    embed.add_field(name="⏱️ Uptime", value=(
        f"**Bot:** {uptime_str}\n"
        f"**VPS:** {str(vps_uptime).split('.')[0]}"
    ), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="cpu")
async def cpu_cmd(ctx):
    cpu = psutil.cpu_percent(interval=1)
    cores = psutil.cpu_count()
    freq = psutil.cpu_freq()
    bar = "█" * int(cpu // 10) + "░" * (10 - int(cpu // 10))
    embed = valakas_embed("🔲 CPU Info")
    embed.add_field(name="Usage", value=f"`[{bar}]` **{cpu}%**", inline=False)
    embed.add_field(name="Cores", value=str(cores), inline=True)
    if freq:
        embed.add_field(name="Frequency", value=f"{freq.current:.0f}MHz", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ram")
async def ram_cmd(ctx):
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    bar = "█" * int(ram.percent // 10) + "░" * (10 - int(ram.percent // 10))
    embed = valakas_embed("💾 RAM Info")
    embed.add_field(name="RAM", value=(
        f"`[{bar}]` **{ram.percent}%**\n"
        f"Used: {ram.used//1024//1024}MB / Total: {ram.total//1024//1024}MB"
    ), inline=False)
    embed.add_field(name="Swap", value=(
        f"Used: {swap.used//1024//1024}MB / Total: {swap.total//1024//1024}MB"
    ), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="disk")
async def disk_cmd(ctx):
    disk = psutil.disk_usage('/')
    bar = "█" * int(disk.percent // 10) + "░" * (10 - int(disk.percent // 10))
    embed = valakas_embed("💿 Disk Info")
    embed.add_field(name="Usage", value=(
        f"`[{bar}]` **{disk.percent}%**\n"
        f"Used: {disk.used//1024//1024//1024}GB / Total: {disk.total//1024//1024//1024}GB\n"
        f"Free: {disk.free//1024//1024//1024}GB"
    ), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime_cmd(ctx):
    uptime_seconds = time.time() - START_TIME
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    vps_uptime = datetime.datetime.now() - boot_time
    embed = valakas_embed("⏱️ Uptime")
    embed.add_field(name="🤖 Bot Uptime", value=uptime_str, inline=True)
    embed.add_field(name="🖥️ VPS Uptime", value=str(vps_uptime).split('.')[0], inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_cmd(ctx):
    latency = round(bot.latency * 1000)
    embed = valakas_embed("🏓 Pong!")
    embed.add_field(name="Latency", value=f"**{latency}ms**")
    await ctx.send(embed=embed)

@bot.command(name="ps")
@is_owner()
async def ps_cmd(ctx):
    procs = []
    for p in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:10]:
        procs.append(
            f"`{p.info['pid']:>6}` | `{p.info['name'][:20]:<20}` | CPU: {p.info['cpu_percent'] or 0:.1f}% | RAM: {p.info['memory_percent'] or 0:.1f}%"
        )
    embed = valakas_embed("📋 Top Processes")
    embed.description = "\n".join(procs) or "No processes found."
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────────────────────
# SHELL COMMANDS
# ─────────────────────────────────────────────────────────────

@bot.command(name="run")
@is_owner()
async def run_cmd(ctx, *, command: str):
    msg = await ctx.send(embed=valakas_embed("⚙️ Running...", f"```{command}```"))
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=30
        )
        output = result.stdout or result.stderr or "No output."
        if len(output) > 1900:
            output = output[:1900] + "\n... [truncated]"
        embed = valakas_embed("✅ Command Output", f"```bash\n$ {command}\n\n{output}```")
        await msg.edit(embed=embed)
    except subprocess.TimeoutExpired:
        await msg.edit(embed=error_embed("Command timed out (30s limit)."))
    except Exception as e:
        await msg.edit(embed=error_embed(str(e)))

@bot.command(name="restart")
@is_owner()
async def restart_cmd(ctx):
    await ctx.send(embed=valakas_embed("🔄 Restarting", "Valakas is restarting..."))
    await asyncio.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

@bot.command(name="reboot")
@is_owner()
async def reboot_cmd(ctx):
    await ctx.send(embed=valakas_embed("⚠️ Rebooting VPS", "The VPS is rebooting now!"))
    await asyncio.sleep(2)
    subprocess.run("reboot", shell=True)

@bot.command(name="update")
@is_owner()
async def update_cmd(ctx):
    msg = await ctx.send(embed=valakas_embed("🔄 Updating VPS", "Running apt update & upgrade..."))
    result = subprocess.run(
        "apt update -y && apt upgrade -y",
        shell=True, capture_output=True, text=True, timeout=300
    )
    output = (result.stdout + result.stderr)[-1800:]
    await msg.edit(embed=valakas_embed("✅ Update Done", f"```{output}```"))

@bot.command(name="install")
@is_owner()
async def install_cmd(ctx, package: str):
    msg = await ctx.send(embed=valakas_embed("📦 Installing", f"Installing `{package}`..."))
    result = subprocess.run(
        f"apt install -y {package}",
        shell=True, capture_output=True, text=True, timeout=120
    )
    output = (result.stdout + result.stderr)[-1800:]
    await msg.edit(embed=valakas_embed(f"✅ Installed {package}", f"```{output}```"))

@bot.command(name="kill")
@is_owner()
async def kill_cmd(ctx, pid: int):
    try:
        p = psutil.Process(pid)
        name = p.name()
        p.kill()
        await ctx.send(embed=success_embed(f"Killed process `{name}` (PID: {pid})"))
    except Exception as e:
        await ctx.send(embed=error_embed(str(e)))

# ─────────────────────────────────────────────────────────────
# DOCKER COMMANDS
# ─────────────────────────────────────────────────────────────

@bot.command(name="dps")
@is_owner()
async def docker_ps(ctx):
    result = subprocess.run("docker ps -a --format '{{.Names}} | {{.Status}} | {{.Image}}'",
                            shell=True, capture_output=True, text=True)
    output = result.stdout or "No containers found / Docker not running."
    embed = valakas_embed("🐳 Docker Containers", f"```{output}```")
    await ctx.send(embed=embed)

@bot.command(name="dstart")
@is_owner()
async def docker_start(ctx, name: str):
    result = subprocess.run(f"docker start {name}", shell=True, capture_output=True, text=True)
    output = result.stdout or result.stderr
    await ctx.send(embed=valakas_embed(f"▶️ Started: {name}", f"```{output}```"))

@bot.command(name="dstop")
@is_owner()
async def docker_stop(ctx, name: str):
    result = subprocess.run(f"docker stop {name}", shell=True, capture_output=True, text=True)
    output = result.stdout or result.stderr
    await ctx.send(embed=valakas_embed(f"⏹️ Stopped: {name}", f"```{output}```"))

@bot.command(name="drestart")
@is_owner()
async def docker_restart(ctx, name: str):
    result = subprocess.run(f"docker restart {name}", shell=True, capture_output=True, text=True)
    output = result.stdout or result.stderr
    await ctx.send(embed=valakas_embed(f"🔄 Restarted: {name}", f"```{output}```"))

@bot.command(name="dlogs")
@is_owner()
async def docker_logs(ctx, name: str):
    result = subprocess.run(f"docker logs --tail=30 {name}", shell=True, capture_output=True, text=True)
    output = (result.stdout + result.stderr)[-1800:] or "No logs."
    await ctx.send(embed=valakas_embed(f"📋 Logs: {name}", f"```{output}```"))

# ─────────────────────────────────────────────────────────────
# FILE COMMANDS
# ─────────────────────────────────────────────────────────────

@bot.command(name="ls")
@is_owner()
async def ls_cmd(ctx, path: str = "."):
    result = subprocess.run(f"ls -la {path}", shell=True, capture_output=True, text=True)
    output = result.stdout or result.stderr
    if len(output) > 1900:
        output = output[:1900] + "\n..."
    await ctx.send(embed=valakas_embed(f"📁 {path}", f"```{output}```"))

@bot.command(name="cat")
@is_owner()
async def cat_cmd(ctx, path: str):
    result = subprocess.run(f"cat {path}", shell=True, capture_output=True, text=True)
    output = result.stdout or result.stderr
    if len(output) > 1900:
        output = output[:1900] + "\n... [truncated]"
    await ctx.send(embed=valakas_embed(f"📄 {path}", f"```{output}```"))

@bot.command(name="mkdir")
@is_owner()
async def mkdir_cmd(ctx, path: str):
    result = subprocess.run(f"mkdir -p {path}", shell=True, capture_output=True, text=True)
    await ctx.send(embed=success_embed(f"Created directory: `{path}`"))

@bot.command(name="rm")
@is_owner()
async def rm_cmd(ctx, path: str):
    result = subprocess.run(f"rm -rf {path}", shell=True, capture_output=True, text=True)
    await ctx.send(embed=success_embed(f"Deleted: `{path}`"))

# ─────────────────────────────────────────────────────────────
# NETWORK COMMANDS
# ─────────────────────────────────────────────────────────────

@bot.command(name="ports")
@is_owner()
async def ports_cmd(ctx):
    result = subprocess.run("ss -tuln", shell=True, capture_output=True, text=True)
    output = result.stdout[-1800:] or "No output."
    await ctx.send(embed=valakas_embed("🌐 Open Ports", f"```{output}```"))

@bot.command(name="netstat")
@is_owner()
async def netstat_cmd(ctx):
    net = psutil.net_io_counters()
    embed = valakas_embed("🌐 Network Stats")
    embed.add_field(name="📤 Sent", value=f"{net.bytes_sent//1024//1024}MB", inline=True)
    embed.add_field(name="📥 Received", value=f"{net.bytes_recv//1024//1024}MB", inline=True)
    embed.add_field(name="📦 Packets Sent", value=str(net.packets_sent), inline=True)
    embed.add_field(name="📦 Packets Recv", value=str(net.packets_recv), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ip")
async def ip_cmd(ctx):
    result = subprocess.run("curl -s ifconfig.me", shell=True, capture_output=True, text=True, timeout=10)
    ip = result.stdout.strip() or "Could not fetch IP"
    await ctx.send(embed=valakas_embed("🌍 Server IP", f"**Public IP:** `{ip}`"))

@bot.command(name="speedtest")
@is_owner()
async def speedtest_cmd(ctx):
    msg = await ctx.send(embed=valakas_embed("⚡ Speedtest", "Running speedtest... (may take 30s)"))
    result = subprocess.run("speedtest-cli --simple", shell=True, capture_output=True, text=True, timeout=60)
    output = result.stdout or result.stderr or "speedtest-cli not installed. Run: `!install speedtest-cli`"
    await msg.edit(embed=valakas_embed("⚡ Speedtest Results", f"```{output}```"))

# ─────────────────────────────────────────────────────────────
# RUN BOT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting Valakas Bot...")
    bot.run(TOKEN)
