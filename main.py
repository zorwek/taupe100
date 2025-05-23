import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Constantes
EMOJI_BLOQUE = "TOP100"
ROLE_AUTORISE_ID = 1375415937393492050

# Intents nécessaires pour le bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if f":{EMOJI_BLOQUE}:" in message.content:
        has_role = any(role.id == ROLE_AUTORISE_ID for role in message.author.roles)
        if not has_role:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, tu ne peux pas utiliser cet emoji sans le bon rôle.",
                delete_after=5
            )
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji_name = reaction.emoji.name if isinstance(reaction.emoji, discord.Emoji) else str(reaction.emoji)
    if emoji_name == EMOJI_BLOQUE:
        guild = reaction.message.guild
        member = guild.get_member(user.id)
        if member is None:
            return

        has_role = any(role.id == ROLE_AUTORISE_ID for role in member.roles)
        if not has_role:
            await reaction.remove(user)
            await reaction.message.channel.send(
                f"{user.mention}, tu n'as pas le droit d'ajouter cette réaction.",
                delete_after=5
            )

# Partie Flask pour garder le bot alive sur Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 10000))  # Render impose ce port, default 10000
    print(f"⚙️ Flask app running on port {port}")
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Démarrage
keep_alive()
bot.run(os.environ["DISCORD_TOKEN"])


