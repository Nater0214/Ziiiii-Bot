# src/bot/cogs/__init__.py
# Load the cogs


# Imports
from .funny import Funny
from .general import General
from .mc import Minecraft


# Definitions
def setup(bot):
    bot.add_cog(Minecraft(bot))
    bot.add_cog(General(bot))
    bot.add_cog(Funny(bot))