# src/bot/cogs/__init__.py
# Load the cogs


# Imports
from .funny import Funny
from .general import General
from .kevin import Kevin
from .mc import Minecraft


# Definitions
def setup(bot):
    bot.add_cog(General(bot))
    bot.add_cog(Kevin(bot))
    bot.add_cog(Minecraft(bot))
    bot.add_cog(General(bot))
    # bot.add_cog(Funny(bot))