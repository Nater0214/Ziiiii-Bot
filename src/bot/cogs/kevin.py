# src/bot/cogs/mc.py
# A cog for Kevin Macleod related commands


import os

# Imports
from discord import ApplicationContext, ButtonStyle, FFmpegPCMAudio, Interaction, Option, ui
from discord.errors import HTTPException
from discord.ext import commands

from lib import kmaudio


# Definitions
class Kevin(commands.Cog):
    """Kevin Macleod commands"""
    
    # Playing value
    playing = False
    
    # Views
    class PlaySongView(ui.View):
        """A view for playing a single song"""
        
        def __init__(self, song_name: str) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Create the button
            button = ui.Button(label="Play", style=ButtonStyle.primary)
            button.callback = self.play_song
            self.add_item(button)
            
            # Set song name
            self.song_name = song_name
        
        # Button method
        async def play_song(self, interaction: Interaction):
            """Play the song"""
            
            # Send the status message
            await interaction.response.edit_message(content=f"Playing {self.song_name}", view=None)
            
            # Get the audio source
            audio_url = kmaudio.search_song(self.song_name, True)
            audio_source = FFmpegPCMAudio(audio_url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-n'}, executable=".\\ffmpeg.exe" if os.name == "nt" else "ffmpeg")
            
            # Play the audio
            try:
                await interaction.guild.voice_client.play(audio_source, after=lambda e: await interaction.guild.voice_client.disconnect())
            except TypeError:
                pass
    
    
    class ResultSelectView(ui.View):
        """A view for selecting a song"""
        
        def __init__(self, query_results: list[str]) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Create the buttons
            for num, result in enumerate(query_results):
                button = ui.Button(label=str(num + 1), style=ButtonStyle.primary, custom_id=str(num))
                button.callback = self.play_song
                self.add_item(button)
            
            # Associate each song with a number
            self.song_nums = {str(num): result for num, result in enumerate(query_results)}
        
        # Button method
        async def play_song(self, interaction: Interaction):
            """Play the selected song"""
            
            # Send the status message
            await interaction.response.edit_message(content=f"Playing {self.song_nums[interaction.custom_id]}", view=None)
            
            # Get the audio source
            audio_url = kmaudio.search_song(self.song_nums[interaction.custom_id], True)
            audio_source = FFmpegPCMAudio(audio_url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-n'}, executable=".\\ffmpeg.exe" if os.name == "nt" else "ffmpeg")
            
            # Play the audio
            try:
                await interaction.guild.voice_client.play(audio_source, after=lambda e: await interaction.guild.voice_client.disconnect())
            except TypeError:
                pass
    
    
    # Commands
    @commands.slash_command(help="Search for and play a Kevin Macleod song by a query")
    async def pkm(self, interaction: ApplicationContext, query: Option(str)):
        """Play a Kevin Macleod song by a query"""
        
        try:
            # Check if something is already playing
            if interaction.guild.voice_client.is_playing():
                await interaction.response.send_message("I'm busy playing a song rn sorry")
                return
            
            # Join the sender's voice channel if the bot isn't already in one
            if interaction.guild.voice_client is None:
                if interaction.user.voice is not None:
                    await interaction.user.voice.channel.connect()
                else:
                    await interaction.response.send_message("You aren't in a VC dumbass")
                    return
            else:
                if interaction.guild.voice_client.channel != interaction.user.voice.channel:
                    await interaction.response.send_message("I'm busy with someone else rn sorry")
                    return
            
            # Acknowledge the command
            await interaction.defer()
            
            # Get the query results
            query_results = kmaudio.search_song(query)
            
            # Respond appropriately
            if len(query_results) > 25:
                await interaction.followup.send("I found too many")
            if len(query_results) > 1:
                await interaction.followup.send("\n".join([f"I found {len(query_results)} songs:", *[f'{num}. {song}' for num, song in enumerate(query_results)]]), view=self.ResultSelectView(query_results))
            elif len(query_results) == 1:
                await interaction.followup.send(f"I found {query_results[0]}", view=self.PlaySongView(query_results[0]))
            else:
                await interaction.followup.send("I found nothing :/")
            
        except HTTPException:
            try:
                await interaction.guild.voice_client.disconnect()
            except AttributeError:
                pass