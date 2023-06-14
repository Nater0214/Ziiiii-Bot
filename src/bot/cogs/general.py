# src/bot/cogs/general.py
# General commands


# Imports
from random import choice

from discord import Interaction
from discord.ext import commands


# Definitions
class General(commands.Cog):
    """General commands"""
    
    # Commands
    @commands.slash_command(help="A friendly greeting")
    async def hello(self, interaction: Interaction):
        """Send a friendly greeting"""
        
        await interaction.response.send_message(choice(["Howdy {}!", "Hello {}!", "Greetings {}!"]).format(interaction.user.display_name))