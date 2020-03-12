from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, member):
        member_id = str(member.author)
        if member_id == 'Lemon Scented Fox#7601':
            await member.add_reaction("\U0001F1E9")
            await member.add_reaction("\U0001F1EE")
            await member.add_reaction("\U0001F1F8")
            await member.add_reaction("\U0001F1F3")
            await member.add_reaction("\U0001F1EA")
            await member.add_reaction("\U0001F1FE")


