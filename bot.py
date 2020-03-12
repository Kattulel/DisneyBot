import discord
from discord.ext import commands as botcmds
from art import *
from colorama import init

init()
from colorama import Fore, Style


def beginload(name):
    print(" - Loading", name, "...")


print(Fore.YELLOW)
discordpy_ver = "Discord.py " + str(discord.__version__)
author_msg = "     Programmed by Kat"
print(text2art("   Disney Bot"))
print(author_msg, discordpy_ver.rjust(33), "\n", Style.RESET_ALL)

beginload("yippi")

beginload("google")

beginload("wiktionaryparser")

beginload("praw")

beginload("google translate")

beginload("keys")
import keys

beginload("commands")
from command.image.reddit import reddit as cmd_reddit
from command.image.birb import birb as cmd_birb
from command.image.cat import cat as cmd_cat
from command.image.food import food as cmd_food
from command.image.e621 import e621 as cmd_e621
from command.image.macro import macro as cmd_macro
from command.help import bothelp as cmd_help
from command.info import usrinfo as cmd_info
from datetime import datetime
from config import usercontrol
import command.audio.music as music
import command.audio.music_menu as music_menu
import command.say as cmd_say
from command.audio.google_voice import langlist as cmd_langlist
from command.audio.overwatch import ow as cmd_ow
from command.audio.overwatch import ow2 as cmd_ow2
#from command.audio.overwatch import name_results as cmd_name_results
bot = botcmds.Bot(command_prefix='!')

beginload("static commands")
import static_commands
bot.add_cog(static_commands.static(bot))

beginload("listeners")
from data import listeners
bot.add_cog(listeners.Listeners(bot))


bot.remove_command("help")
startTime = datetime.now()


@bot.event
async def on_ready():
    connections = bot.guilds
    print(Style.BRIGHT + Fore.GREEN + '\n [!] Connections: ')
    for i in connections:
        print(Style.BRIGHT + Fore.GREEN + '   -> ' + i.name)

    print(Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + ' @ Ready!' + Style.RESET_ALL)

# ~ BOT COMMANDS ~

@bot.command()
async def help(ctx, command=None):
    await cmd_help(ctx, command)

# Message Commands


@bot.command()
async def langlist(ctx):
    await cmd_langlist(ctx)


# Image Related Commands


@bot.command()
async def reddit(ctx, subreddit, keywords=None):
    await cmd_reddit(ctx, subreddit, keywords)


@bot.command()
async def birb(ctx):
    await cmd_birb(ctx)


@bot.command()
async def cat(ctx):
    await cmd_cat(ctx)


@bot.command()
async def food(ctx):
    await cmd_food(ctx)


@bot.command()
async def e621(ctx, *tags):
    await cmd_e621(ctx, *tags)


@bot.command()
async def macro(ctx):
    await cmd_macro(ctx)

# Admin Commands


@bot.command()
async def info(ctx):
    await cmd_info(ctx, startTime)


@bot.command()
async def admin(ctx):
    await usercontrol.admin(ctx)

# Audio Related


@bot.command()
async def ow(ctx, char_name, *audio_name):
    await cmd_ow(ctx, char_name, *audio_name)


# @bot.command()
# async def listvc(ctx, char_name):
#     await cmd_name_results(ctx, char_name)


@bot.command()
async def ow2(ctx, char_name, *audio_name):
    await cmd_ow2(ctx, char_name, *audio_name)


@bot.command()
async def say(ctx, lang, message):
    await cmd_say.say(ctx, lang, message)


@bot.command()
async def sayslow(ctx, lang, message):
    await cmd_say.sayslow(ctx, lang, message)


@bot.command()
async def play(ctx, *args):
    global is_playing
    await music.play(ctx, *args)
    is_playing = True


@bot.command()
async def stop(ctx):
    await music.stop(ctx)


# Events


@bot.event
async def on_reaction_add(reaction, user):
    voice_client = user.guild.voice_client

    if voice_client is not None:
        if not user.bot:
            await music_menu.button_onClick(reaction, voice_client)

    if not user.id == 660195414397681695:
        message = reaction.message
        if reaction.emoji == "❌":
            await message.delete()
            print("Deleted Message: ", message.content)


@bot.event
async def on_reaction_remove(reaction, user):
    voice_client = user.guild.voice_client
    if voice_client is not None:
        if not user.bot:
            await music_menu.button_onClick(reaction, voice_client)

bot.run(keys.discord)
