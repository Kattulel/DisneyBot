import discord
import yaml

with open("data/users.yaml", "r") as ymlfile:
    users = yaml.load(ymlfile, Loader=yaml.BaseLoader)


def find(ctx, typ):
    for i in users[typ]:
        if str(i) == str(ctx.message.author):
            return True
    return False


async def check_admin(ctx):
    if find(ctx, "admin"):
        return True
    else:
        await ctx.send("You can't use **admin** commands.")
        return False


async def admin(ctx):
    return await check_admin(ctx)
