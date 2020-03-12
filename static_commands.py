import random
from discord.ext import commands

class static(commands.Cog):
    @commands.command()
    async def bigF(self, ctx):
        msg = ("███████╗\n"
               "██╔════╝\n"
               "█████╗  \n"
               "██╔══╝  \n"
               "██║     \n"
               "╚═╝     ")
        await ctx.send(msg)

    @commands.command()
    async def yn(self, ctx):
        await ctx.send(random.choice(['Yes', 'No']))

    @commands.command()
    async def roll(self, ctx):
        await ctx.send(random.randint(0, 100))
