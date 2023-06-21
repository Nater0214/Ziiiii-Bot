# src/bot/cogs/mc.py
# A cog for Kevin Macleod related commands


# Imports
from discord import Interaction, Option, FFmpegPCMAudio
from discord.ext import commands

from lib import kmaudio


# Definitions
class Kevin(commands.Cog):
    """Kevin Macleod commands"""
    
    # Playing value
    playing = False
    
    # Commands
    @commands.slash_command(help="Search for and play a Kevin Macleod song by a query")
    async def pkm(self, ctx: commands.Context, query: Option(str)):
        """Play a Kevin Macleod song by a query"""
        
        # Join the sender's voice channel if the bot isn't already in one
        if ctx.voice_client is None:
            if ctx.author.voice.channel is not None:
                vc = await ctx.author.voice.channel.connect()
            else:
                await ctx.reply("You aren't in a VC dumbass")
                return
        else:
            await ctx.reply("I'm busy rn sorry")
            return
        
        query_results = kmaudio.search_song(query)
        if len(query_results) > 1:
            ctx.reply(f"I found {len(query_results)} songs:\n{'\n'.join([f'{num}. {song}' for num, song in enumerate(query_results)])}")
        elif len(query_results) == 1:
            ctx.reply(f"I found {query_results[0]}")
        else:
            ctx.reply("I found nothing :/")