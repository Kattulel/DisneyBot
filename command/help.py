import discord
import yaml

prefix = "!"

ico = {
    "default": "\U0001F539",
    "image": "\U0001F5BC ",
    "text": "\U0001F4C4 ",
    "dot": "\U000025AB ",
    "info": "\U00002139 ",
    "example": "\U000025FB ",
    "audio": "\U0001F3B5 "
}


def style(typ, txt):
    # Discord Text Style, b = bold, i = italic...
    s = {
        "b": "**",  # bold
        "i": "_",  # italic
        "ex": "`"  # One line code, in this case, used for examples.
    }
    # Return of the function depending on the type(typ)
    # See types below:
    return {
        'title': s["b"] + txt + s["b"],
        'desc': "         - " + s["i"] + txt + s["i"],
        'detail': s["i"] + txt + s["i"],
        'example': s["ex"] + txt + s["ex"],
    }[typ]


with open("docs/help.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)


def makelist():
    info = list()
    string = str()

    for cmd in cfg:
        if not cfg[cmd]['type'] == "":
            icon = ico[cfg[cmd]['type']]
        else:
            icon = ico['default']

        command = icon + style("title", prefix + cmd + " " + cfg[cmd]['args'])
        descr = style("desc", cfg[cmd]['description'])
        info.append(command)
        info.append(descr)

    for line in info:
        string = string + line + "\n"

    return string


def get_command_help(cmd):
    if cmd.startswith("!"):
        cmd = cmd.replace("!", "")

    if not cfg[cmd]['type'] == "":
        icon = ico[cfg[cmd]['type']]
    else:
        icon = ico['default']

    command = style("title", prefix + cmd)
    args = style("title", cfg[cmd]['args'])
    desc = cfg[cmd]['description']
    detail = style("detail", "@ " + cfg[cmd]['detailed'])
    example = style("example", prefix + cfg[cmd]['example'])

    string = \
        icon + " " + command + " " + args + \
        "  " + desc + "\n" + \
        detail + "\n" + \
        "\t\t" + ico['dot'] + " Usage:  " + example
    return string


async def bothelp(ctx, command=None):
    if command is None:
        message = makelist()
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name="Avaliable Commands:", value=message, inline=False)
        await ctx.send(embed=embed)
    else:
        try:
            message = get_command_help(command)
            await ctx.send(message)
        except KeyError:
            await ctx.send("Detailed help for that command is **unavaliable.**")


