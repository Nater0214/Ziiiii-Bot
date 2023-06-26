# src/bot/cogs/mc.py
# A cog for Kevin Macleod related commands


# Imports
import os

from discord import ApplicationContext, ButtonStyle, FFmpegPCMAudio, HTTPException, Interaction, Option, SlashCommandGroup, ui
from discord.ext.commands import Cog

from lib import kmaudio


# Definitions
class Kevin(Cog):
    """Kevin Macleod commands"""
    
    # Command group
    command_group = SlashCommandGroup("kevin", "Kevin Macleod commands", guild_ids=[os.getenv("GUILD_ID")])
    
    
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
            interaction.guild.voice_client.play(audio_source)
    
    
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
            interaction.guild.voice_client.play(audio_source)
    
    
    # Commands
    @command_group.command(guild_only=True)
    async def search(self, ctx: ApplicationContext, query: Option(str, description="The query used to find the song")):
        """Play a Kevin Macleod song by a query"""
        
        try:            
            # Do stuff based on voice state
            if ctx.guild.voice_client is None:
                if ctx.user.voice is not None:
                    await ctx.user.voice.channel.connect()
                else:
                    await ctx.response.send_message("You aren't in a VC dumbass")
                    return
            else:
                if ctx.guild.voice_client.is_playing():
                    await ctx.response.send_message("I'm busy playing a song rn sorry")
                    return
                elif ctx.guild.voice_client.channel != ctx.user.voice.channel:
                    await ctx.response.send_message("I'm busy with someone else rn sorry")
                    return
            
            # Acknowledge the command
            await ctx.defer()
            
            # Get the query results
            query_results = kmaudio.search_song(query)
            
            # Respond appropriately
            if len(query_results) > 10:
                await ctx.followup.send("I found too many")
            elif len(query_results) > 1:
                await ctx.followup.send("\n".join([f"I found {len(query_results)} songs:", *[f'{num}. {song}' for num, song in enumerate(query_results)]]), view=self.ResultSelectView(query_results))
            elif len(query_results) == 1:
                await ctx.followup.send(f"I found {query_results[0]}", view=self.PlaySongView(query_results[0]))
            else:
                await ctx.followup.send("I found nothing :/")
            
        except HTTPException:
            try:
                await ctx.guild.voice_client.disconnect()
            except AttributeError:
                pass
    
    
    @command_group.command(guild_only=True)
    async def stop(self, ctx: ApplicationContext, disconnect: Option(bool, description="Wether I should disconnect from the vc") = False):
        """Stop a playing Kevin Macleod Song"""
        
        # Do stuff based on voice state
        if ctx.guild.voice_client is None:
            await ctx.response.send_message("I'm not even in a vc")
        else:
            if ctx.guild.voice_client.is_playing():
                ctx.guild.voice_client.stop()
                if disconnect:
                    await ctx.guild.voice_client.disconnect()
                    await ctx.response.send_message("Bye")
                else:
                    await ctx.response.send_message("Stopped")
            elif ctx.guild.voice_client.channel != ctx.user.voice.channel:
                await ctx.response.send_message("You're in a different vc!")
            elif disconnect:
                await ctx.guild.voice_client.disconnect()
                await ctx.response.send_message("Bye")