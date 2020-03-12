import command.audio.google_voice as googlevoice
import discord
from googletrans import Translator
from googletrans import LANGUAGES
import asyncio

languages = googlevoice.getlangs()


async def recursiveTryToLeave(server):
    if not server.is_playing():
        await asyncio.sleep(1.5)
        await server.disconnect()  # disconnect
        print("Disconnected from VoiceChat!.")
    else:
        await asyncio.sleep(1.5)
        await recursiveTryToLeave(server)


async def say(ctx, lang, *message):
    string = message
    avaliable = bool()

    lang = lang

    if lang == "?":
        msg = message
        avaliable = False
        # Detect Language ... / get language
        translator = Translator()
        lang = translator.detect(msg)
        print("Detected! -> ", lang.lang, lang.confidence)
        lang = lang.lang

        # Check if lang code is correct and adjust it if not
        if not len(lang) < 3:
            if "-" not in lang:
                lang = str(lang)[:2]

        # check if the language is avaliable for voice output (Google)
        for key, value in languages.items():
            if key == lang:
                avaliable = True
                break
            avaliable = False

        # if language is unavaliable...
        if not avaliable:
            msg = LANGUAGES[lang].capitalize() + " language is unavaliable."
            await ctx.send(msg)

    else:
        # user selected a language
        if googlevoice.checkLanguage(lang):
            msg = string.replace("!say " + lang, "")
            print("Google Voice:", lang, msg)
            googlevoice.make_audio(msg, lang)
            avaliable = True
        else:
            msg = "Unable to find langcode: **" + str(lang) + "** please consider using **!langlist** command."
            await ctx.send(msg)

    if avaliable:
        googlevoice.make_audio(msg, lang)
        audio_scr = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="audio.mp3")
        volume_adjusted = discord.PCMVolumeTransformer(audio_scr, volume=float(0.5))
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild.voice_client
        await asyncio.sleep(1.5)
        server.play(volume_adjusted)
        await recursiveTryToLeave(server)


async def sayslow(ctx, lang, *message):
    string = message
    avaliable = bool()

    lang = lang

    if lang == "?":
        msg = message
        avaliable = False
        # Detect Language ... / get language
        translator = Translator()
        lang = translator.detect(msg)
        print("Detected! -> ", lang.lang, lang.confidence)
        lang = lang.lang

        # Check if lang code is correct and adjust it if not
        if not len(lang) < 3:
            if "-" not in lang:
                lang = str(lang)[:2]

        # check if the language is avaliable for voice output (Google)
        for key, value in languages.items():
            if key == lang:
                avaliable = True
                break
            avaliable = False

        # if language is unavaliable...
        if not avaliable:
            msg = LANGUAGES[lang].capitalize() + " language is unavaliable."
            await ctx.send(msg)

    else:
        # user selected a language
        if googlevoice.checkLanguage(lang):
            msg = string.replace("!say " + lang, "")
            print("Google Voice:", lang, msg)
            googlevoice.make_audio(msg, lang)
            avaliable = True
        else:
            msg = "Unable to find langcode: **" + str(lang) + "** please consider using **!langlist** command."
            await ctx.send(msg)

    if avaliable:
        googlevoice.make_audio_slow(msg, lang)
        audio_scr = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="audio.mp3")
        volume_adjusted = discord.PCMVolumeTransformer(audio_scr, volume=float(0.5))
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild.voice_client
        await asyncio.sleep(1.5)
        server.play(volume_adjusted)
        await recursiveTryToLeave(server)

