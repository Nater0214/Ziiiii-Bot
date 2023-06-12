# src/bot/__init__.py
# Bot stuff


# Imports
from os import environ
import asyncio

from discord import Intents
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
    bot = commands.Bot(command_prefix="z!", intents=intents)
    
    # Add loop event
    @bot.event
    async def on_ready() -> None:
        main_loop()
    
    # Add cogs
    bot.load_extension("src.bot.cogs")
    
    # Run the bot
    bot.run(environ.get("BOT_TOKEN"))