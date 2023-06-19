# src/bot/cogs/mc.py
# A cog for minecraft server commands


# Imports
import multiprocessing
import subprocess

from discord import Interaction
from discord.ext import commands


# Definitions
class Minecraft(commands.Cog):
    """Minecraft commands"""
    
    # Commands
    @commands.slash_command(help="Starts a minecraft server")
    async def startmc(self, interaction: Interaction, server: str = "blox-smp"):
        """Starts a minecraft server"""
        
        # Define server starting method
        def start_server(*command: list) -> None:
            """Run a command to start a server"""
            
            # Run the command
            subprocess.Popen(["nohup", *command, ">", "/dev/null", "&"])
        
        # Check for valid server name
        if not server in ["blox-smp"]:
            await interaction.response.send_message("Invalid server name")
            return
        
        # Send status message
        await interaction.response.send_message(f"Starting minecraft server {server}...")
        
        # Start the server
        if server == "blox-smp":
            multiprocessing.Process(target=start_server, args=["/var/mc-servers/blox_smp_1/run.sh", "y"]).start()
    
    
    @commands.slash_command(help="Lists all minecraft servers")
    async def listmc(self, interaction: Interaction):
        """Lists all minecraft servers"""
        
        await interaction.response.send_message("All Minecraft Servers:\n `blox-smp`: The Blox SMP\nThats it lol")