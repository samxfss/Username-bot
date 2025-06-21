import discord
import requests
import time
import asyncio
import random
import string

# ⚠️ INSERT YOUR DISCORD BOT TOKEN HERE
TOKEN = ''  # Never share your token publicly!

# Optional letter-to-number replacements for similar variations
SIMILAR_CHARS = {
    'a': ['4'], 'b': ['8'], 'e': ['3'], 'g': ['6'],
    'i': ['1'], 'l': ['1'], 'o': ['0'], 's': ['5'],
    't': ['7'], 'z': ['2'],
}

# 🎯 Set up Discord bot with permissions to read messages
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# 🔤 Generates a random username with given length (letters + digits)
def generate_random_username(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

# ✅ Check if a Roblox username is available
def check_username(username):
    url = f"https://auth.roblox.com/v2/usernames/validate?request.username={username}&request.birthday=2000-01-01"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # code 0 = valid (username is available)
            return data["code"] == 0
        else:
            return False
    except:
        return False

# ✅ Bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# 💬 Handle messages/commands
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 📌 Help menu
    if message.content.startswith("!help"):
        help_text = """
📌 **Roblox Username Bot — Commands**

`!check <username>` — Check availability (with leetspeak variations)
`!gen5` — Generate 5-letter usernames
`!gen6` — Generate 6-letter usernames
`!gen <length> <amount>` — Custom-length usernames
`!ping` — Show bot latency
`!about` — Info about this bot
`!invite` — Get bot invite link
`!randomname` — Suggest funny display names
"""
        await message.channel.send(help_text)

    # 🔍 Check specific username
    elif message.content.startswith("!check"):
        try:
            base = message.content.split(" ", 1)[1].lower().strip()
        except IndexError:
            await message.channel.send("⚠️ Usage: `!check <username>`")
            return

        await message.channel.send(f"🔍 Checking availability for `{base}` and similar variations...")

        variations = set([base])
        for i, char in enumerate(base):
            if char in SIMILAR_CHARS:
                for replacement in SIMILAR_CHARS[char]:
                    new_username = base[:i] + replacement + base[i+1:]
                    variations.add(new_username)

        found = False

        for username in variations:
            await asyncio.sleep(0.3)
            if check_username(username):
                print(f"! VALID: {username}")  # <-- You will see this when a valid username is found!
                found = True
                embed = discord.Embed(
                    title="✅ Available Roblox Username Found!",
                    description=f"```{username}```",
                    color=0x1abc9c
                )
                embed.set_footer(text="Made by S-A-M-X")
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)

        if not found:
            await message.channel.send("❌ No available variations found.")

    # 🔄 Generate 5-letter usernames
    elif message.content.startswith("!gen5"):
        await message.channel.send("🎲 Generating 5 letter Roblox usernames...")

        for _ in range(5):
            uname = generate_random_username(5)
            await asyncio.sleep(0.3)
            if check_username(uname):
                print(f"! VALID: {uname}")
                embed = discord.Embed(
                    title="✅ 5-letter Available Username Found",
                    description=f"```{uname}```",
                    color=0x7289da
                )
                embed.set_footer(text="Made by S-A-M-X")
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)

    # 🔄 Generate 6-letter usernames
    elif message.content.startswith("!gen6"):
        await message.channel.send("🎲 Generating 6 letter Roblox usernames...")

        for _ in range(5):
            uname = generate_random_username(6)
            await asyncio.sleep(0.3)
            if check_username(uname):
                print(f"! VALID: {uname}")
                embed = discord.Embed(
                    title="✅ 6-letter Available Username Found",
                    description=f"```{uname}```",
                    color=0x2ecc71
                )
                embed.set_footer(text="Made by S-A-M-X")
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)

    # 🧠 Custom username generator: !gen <length> <amount>
    elif message.content.startswith("!gen "):
        parts = message.content.split()
        if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
            await message.channel.send("⚠️ Usage: `!gen <length> <amount>` (e.g. `!gen 5 10`)")
            return

        length = int(parts[1])
        amount = int(parts[2])

        await message.channel.send(f"🎲 Generating {amount} usernames of length {length}...")

        for _ in range(amount):
            uname = generate_random_username(length)
            await asyncio.sleep(0.3)
            if check_username(uname):
                print(f"! VALID: {uname}")
                embed = discord.Embed(
                    title=f"✅ {length}-letter Available Username Found",
                    description=f"```{uname}```",
                    color=0x3498db
                )
                embed.set_footer(text="Made by S-A-M-X")
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)

    # 🏓 Ping command
    elif message.content.startswith("!ping"):
        latency = round(bot.latency * 1000)
        await message.channel.send(f"🏓 Pong! Latency: `{latency}ms`")

    # 🤖 About the bot
    elif message.content.startswith("!about"):
        embed = discord.Embed(
            title="🤖 About This Bot",
            description="Finds available Roblox usernames using letters & digits.",
            color=0x95a5a6
        )
        embed.add_field(name="Creator", value="Made by xmsfs / S-A-M-X")
        embed.add_field(name="Language", value="Python (discord.py)")
        embed.set_footer(text="Happy username hunting!")
        await message.channel.send(embed=embed)

    # 🔗 Invite link
    elif message.content.startswith("!invite"):
        await message.channel.send("🔗 Invite me to your server:\nhttps://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot")

    # 🤣 Funny display name suggestion
    elif message.content.startswith("!randomname"):
        funny_names = [
            "NoobMaster69", "MrBanHammer", "oofinator9000",
            "BuilderBro", "SussyBlox", "YeetMaster", "CringeKing"
        ]
        await message.channel.send(f"🤣 Try this name: `{random.choice(funny_names)}`")

# 🔁 Start the bot
bot.run(TOKEN)