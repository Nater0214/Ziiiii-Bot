# src/bot/__init__.py
# Bot stuff


# Imports
from os import environ

from discord import Intents, Activity, ActivityType, Member, VoiceState
from discord.ext import commands

from .src import main_loop


# Definitions
def run() -> None:
    """Run the bot"""
    
    # Set bot intents
    intents = Intents.default()
    intents.typing = False
    intents.message_content = True
    intents.presences = False
    
    # Create bot
    bot = commands.Bot(intents=intents, help_command=None)
    bot.activity = Activity(type=ActivityType.watching, name="Backflipblox")
    
    # Add loop event
    @bot.event
    async def on_ready() -> None:
        main_loop()
    
    # Add voice event
    @bot.event
    async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
        if member.id != 1110972509572050985:
            if after.channel is None:
                await member.guild.voice_client.disconnect()
    
    # Add cogs
    bot.load_extension("src.bot.cogs")
    
    # Run the bot
    print("Starting the bot")
    bot.run(environ.get("BOT_TOKEN"))