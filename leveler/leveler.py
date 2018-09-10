import discord
from discord.ext import commands
from random import randint

minMessageScore = 0
maxMessageScore = 100

class Leveler:
    async def on_message(self, message):
        print(randint(minMessageScore, maxMessageScore))
        print(message)

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Leveler(bot))
