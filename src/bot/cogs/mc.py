# src/bot/src/cogs/mc.py
# A cog for minecraft server commands


# Imports
from discord import Interaction
from discord.ext import commands
import subprocess


# Definitions
class Minecraft(commands.Cog):
    """Minecraft commands"""
    
    # Commands
    @commands.slash_command(help="Starts a minecraft server")
    async def startmc(self, interaction: Interaction, server: str):
        """Starts a minecraft server"""
        
        # Check for valid server name
        if not server in ["blox-smp"]:
            await interaction.response.send_message("Invalid server name")
            return
        
        # Send status message
        await interaction.response.send_message(f"Starting minecraft server {server}...")
        
        # Start the server
        if server == "blox-smp":
            subprocess.run(["/var/mc-servers/blox_smp_1/start.sh", "y"])
    
    
    @commands.slash_command(help="Starts a minecraft server")
    async def listmc(self, interaction: Interaction, server: str):
        """Starts a minecraft server"""
        
        # Check for valid server name
        if not server in ["blox-smp"]:
            await interaction.response.send_message("Invalid server name")
            return
        
        # Send status message
        await interaction.response.send_message(f"Starting minecraft server {server}...")
        
        # Start the server
        if server == "blox-smp":
            subprocess.run(["/var/mc-servers/blox_smp_1/start.sh", "y"])
    
    
    @commands.slash_command(help="Lists all minecraft servers")
    async def listmc_(self, interaction: Interaction):
        """Lists all minecraft servers"""
        
        await interaction.response.send_message("All Minecraft Servers:\n `blox-smp`: The Blox SMP\nThats it lol")