# src/bot/cogs/funny.py
# Funny commands


# Imports
from discord import Interaction
from discord.ext import commands
from ytmusicapi import ytmusic

YTMusic = ytmusic.YTMusic()


# Definitions
class Funny(commands.Cog):
    """Funny commands"""
    
    # Commands
    @commands.slash_command(help="Play a random Kevin Macleod song")
    async def rkm(self, interaction: Interaction):
        """Play a random Kevin Macleod song"""
        
        kevin = YTMusic.get_artist("UCBqb0wSlWVFBnSuTI3Tcxig")
        
        interaction.response.send_message(f"Here is Kevin's data:\n```{kevin}```")