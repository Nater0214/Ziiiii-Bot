# src/bot/cogs/mc.py
# A cog for Kevin Macleod related commands


# Imports
from discord import ApplicationContext, Option
from discord.ext import commands

from lib import kmaudio


# Definitions
class Kevin(commands.Cog):
    """Kevin Macleod commands"""
    
    # Playing value
    playing = False
    
    # Commands
    @commands.slash_command(help="Search for and play a Kevin Macleod song by a query")
    async def pkm(self, interaction: ApplicationContext, query: Option(str)):
        """Play a Kevin Macleod song by a query"""
        
        # Join the sender's voice channel if the bot isn't already in one
        if interaction.guild.voice_client is None:
            if interaction.user.voice is not None:
                vc = await interaction.user.voice.channel.connect()
            else:
                await interaction.response.send_message("You aren't in a VC dumbass")
                return
        else:
            await interaction.response.send_message("I'm busy rn sorry")
            return
        
        # Acknowledge the command
        await interaction.defer()
        
        # Get the query results
        query_results = kmaudio.search_song(query)
        
        # Respond appropriately
        if len(query_results) > 1:
            await interaction.followup.send("\n".join([f"I found {len(query_results)} songs:", *[f'{num}. {song}' for num, song in enumerate(query_results)]]))
        elif len(query_results) == 1:
            await interaction.followup.send(f"I found {query_results[0]}")
        else:
            await interaction.followup.send("I found nothing :/")
        
        # Leave the voice channel
        await vc.disconnect()