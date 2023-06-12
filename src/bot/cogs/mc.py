# src/bot/src/cogs/mc.py
# A cog for minecraft server commands


# Imports
from discord import Interaction
from discord.ext import commands


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
        
        await interaction.response.send_message(f"Starting minecraft server {server}...")