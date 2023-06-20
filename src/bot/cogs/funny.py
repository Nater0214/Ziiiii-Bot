# src/bot/cogs/funny.py
# Funny commands


# Imports
from os import getenv

from discord import Interaction
from discord.ext import commands


# Definitions
class Funny(commands.Cog):
    """Funny commands"""
    
    # Commands
    @commands.slash_command(help="Play a random Kevin Macleod song", guild_ids=[getenv("GUILD_ID")])
    async def rkm(self, interaction: Interaction):
        """Play a random Kevin Macleod song"""
        
        interaction.response.send_message("Sorry I dont work yet")