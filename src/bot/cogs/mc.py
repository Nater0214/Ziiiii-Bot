# src/bot/cogs/mc.py
# A cog for minecraft server commands


# Imports
from os import getenv
import subprocess

from discord import Interaction
from discord.ext.commands import slash_command
from discord import Option, SlashCommandGroup


# Definitions
class Minecraft(commands.Cog):
    """Minecraft commands"""
    
    # Command group
    command_group = SlashCommandGroup("mc", "Minecraft commands", guild_ids=[getenv("GUILD_ID")])
    
    # Commands
    @command_group.command(help="Starts a minecraft server", guild_ids=[getenv("GUILD_ID")], guild_only=True)
    async def start(self, interaction: Interaction, server: Option(str)):
        """Starts a minecraft server"""
        
        # Check for valid server name
        if not server in ["blox-smp"]:
            await interaction.response.send_message("Invalid server name")
            return
        
        # Send status message
        await interaction.response.send_message(f"Starting minecraft server {server}...")
        
        # Start the server
        if server == "blox-smp":
            subprocess.Popen(["/var/mc-servers/blox_smp_1/run.sh", "y"])
    
    
    @command_group.command(help="Lists all minecraft servers", guild_ids=[getenv("GUILD_ID")], guild_only=True)
    async def list(self, interaction: Interaction):
        """Lists all minecraft servers"""
        
        await interaction.response.send_message("All Minecraft Servers:\n `blox-smp`: The Blox SMP\nThats it lol")