# src/bot/cogs/__init__.py
# Load the cogs


# Imports
from .funny import Funny
from .general import General
from .mc import Minecraft
from .kevin import Kevin


# Definitions
def setup(bot):
    bot.add_cog(Minecraft(bot))
    bot.add_cog(General(bot))
    bot.add_cog(Funny(bot))
    bot.add_cog(Kevin(bot))