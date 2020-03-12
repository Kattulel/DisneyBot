from command.audio.youtube import YTDLSource
from command.audio.youtube import getTitle
import command.audio.music_menu as music_menu
import discord
import os.path


def verify_type(arg):
    if "https://" or "youtube" in arg:
        return 'link'
    return 'volume'


async def connect(ctx):
    if ctx.author.voice is not None and ctx.author.voice.channel is not None:
        channel = ctx.author.voice.channel
        await channel.connect()
        return ctx.guild.voice_client


def check_file():
    if os.path.exists("data/song.mp3"):
        os.remove("data/song.mp3")


async def dl_youtube(url):
    print("Downloading..", url)
    await YTDLSource.from_url(url)
    print("Finished..", url)


async def stop(ctx):
    if ctx.author.voice is not None and ctx.author.voice.channel is not None:
        channel = ctx.guild.voice_client
        await channel.disconnect()


async def pause_music(vc):
    if vc is not None:
        await vc.pause()


async def resume_music(vc):
    if vc is not None:
        await vc.resume()


async def stop_music(channel):
    if channel is not None:
        await channel.disconnect()


async def play(ctx, *args):
    volume, url = args[0], str()

    if not ctx.author.voice or not ctx.author.voice.channel:
        ctx.send("You are not connected to any voice channel.")
        return

    argtype = verify_type(volume)
    if argtype == 'link':
        volume, url = 1.0, args[0]
    else:
        volume, url = args[0], args[1]

    title = getTitle(url)

    check_file()
    await dl_youtube(url)
    volume = float(volume) * 0.25
    audio_scr = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="data/song.mp3")
    volume_adjusted = discord.PCMVolumeTransformer(audio_scr, volume=float(volume))
    server = await connect(ctx)
    server.play(volume_adjusted)
    await music_menu.genMusicMenu(ctx, title)
    print("Playing...", url)
