import asyncio
import ssl
import traceback
import urllib.request
import discord

import requests
from bs4 import BeautifulSoup
import difflib
from urllib.parse import unquote
import google
from google import google
import re
from requests import get as __get
from data.overwatch_charnames import names as ow_char_names
from logger import blog


class UnableToFindVoiceLine(Exception):
    pass


class CantGuessName(Exception):
    pass


def correct_charname(char_name):
    scores = [[], []]
    for name in ow_char_names:
        score = difflib.SequenceMatcher(None, char_name, name.lower()).ratio()
        scores.append([score, name])

    _max = scores.index(max(scores))
    if scores[_max][0] < 0.35:
        raise CantGuessName

    print("Max:", scores[_max][1], scores[_max][0])
    return scores[_max][1]


def get_url_owpedia(text):
    url = "https://overwatch.gamepedia.com/api.php?action=opensearch&format=json&formatversion=2&search=" + text + \
          "&namespace=0&limit=10&suggest=true"
    r = requests.get(url=url)
    liztz = r.text.replace('"', "").replace("]", "").replace("[", "").split(",")
    for i in liztz:
        if "/Quotes" in i and "https://" in i:
            return i


async def recursiveTryToLeave(server):
    if not server.is_playing():
        await asyncio.sleep(1.5)
        await server.disconnect()  # disconnect
        print("Disconnected from VoiceChat!.")
    else:
        await asyncio.sleep(1.5)
        await recursiveTryToLeave(server)


def get_audios(char_name):
    url = get_url_owpedia(char_name)
    html = __get(url).text
    soup = BeautifulSoup(html, 'lxml')
    audios = list()

    for i in soup.findAll('tr'):
        audios.append(i)
    fixed_audios = []

    for i in range(0, len(audios)):
        x = audios[i].find_all('td')

        audio = None
        name = None

        for i in x:
            if "rowspan" in str(i):
                continue
            if "<b>" in str(i):
                continue

            name = i.text
            if "https://" not in name:
                break

        # get audio

        for i in x:
            if "rowspan" in str(i):
                continue

            audio = i.find("audio")

            if audio is not None:
                audio = audio.get("src")

        if audio is not None and name is not None:
            fixed_audios.append([name, audio])

    #sanitize
    for i in range(0, len(fixed_audios)):
        name = str(fixed_audios[i][0])

        if name.startswith("\n"):
            name = name.split('\n', 1)[1]

        if "\n" in name:
            name = name.split('\n', 1)[0]
            name = name.replace("\n", "")

        if "] " in name:
            name = name.split('] ', 1)[1]
        elif "]" in name:
            name = name.split(']', 1)[1]

        if "https://" in name:
            name = name.split('File:', 1)[1]
            name = name.replace("_", " ")
            name = name[:-4]

        fixed_audios[i][0] = name.lower()

    return fixed_audios


def url_find(audios_list, audio_name):
    scores = []
    for i in range(0, len(audios_list)):
        curr_name = audios_list[i][0]
        score = difflib.SequenceMatcher(None, audio_name, curr_name).ratio()
        scores.append([score, i])

    _max = scores.index(max(scores))

    if scores[_max][0] < 0.35:
        raise UnableToFindVoiceLine

    return audios_list[_max][1]


async def name_results(ctx, char):
    links = get_audios(char)
    audio_names = list()
    # Get audio names
    for i in links:
        if len(i) > 0:
            audio_names.append([i[0]])

    msg = ""
    for i in audio_names:
        msg = msg + i[0] + "\n"

    n = 2000
    chunks = [msg[i:i + n] for i in range(0, len(msg), n)]
    for i in chunks:
        await ctx.send(i)


def get_servertwo(char_name, audio_name):
    audio_names = list()
    words = list()
    curr = list()
    list_of_matches = list()
    possibilities = audio_name.lower().split(" ")

    # Find URL:
    search_results = google.search("esportstales " + char_name + " voice lines", 1)
    query_result = ""

    for result in search_results:
        query_result = result.link
        if not query_result == '':
            break

    URL = query_result
    page = requests.get(URL)
    print(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    audio_list = list()

    for link in soup.findAll("div", {"class": "sqs-audio-embed"}):
        audio_list.append([link.get('data-url'), link.get("data-title").lower()])

    for i, item in enumerate(audio_list):
        text = item[1]
        words.append([i, text.split(" ")])

    for i, word in enumerate(words):
        # curr_word = list with the words separated
        curr_word = words[i][1]

        # Check for similarity
        matches = list()
        for _word in curr_word:
            matched_results = difflib.get_close_matches(_word, possibilities, cutoff=0.68)

            if len(matched_results) > 0:
                matches.append(matched_results)
                # list_of_matches.append([" ".join(words[i][1]), match_list])

        if len(matches) > 0:
            list_of_matches.append([" ".join(words[i][1]), matches, i])

    for i in list_of_matches:
        print(i)

    for i in list_of_matches:
        if len(i[1]) > len(possibilities) - 1:
            return str(audio_list[i[2]][0])


def get(char, audio_name):
    x = get_audios(char)
    v = url_find(x, audio_name)
    return v


@blog()
async def ow(ctx, char_name, *audio_name):
    try:
        audio_name = str.join(" ", audio_name)
        ssl._create_default_https_context = ssl._create_unverified_context
        print(char_name, audio_name)
        character = correct_charname(char_name)
        url = get(character, audio_name)
        file_name = "data/vc." + url.split(".")[-1]
        urllib.request.urlretrieve(url, file_name)
        audio_scr = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=file_name)
        volume_adjusted = discord.PCMVolumeTransformer(audio_scr, volume=float(0.5))
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild.voice_client
        await asyncio.sleep(1.5)
        server.play(volume_adjusted)
        await recursiveTryToLeave(server)
    except UnableToFindVoiceLine:
        await ctx.send("cant find the voice line for " + str([char_name, audio_name]), delete_after=10)
    except CantGuessName:
        await ctx.send("cant guess the name disney, try again", delete_after=10)
    except Exception:
        print(traceback.format_exception())


async def ow2(ctx, char_name, *audio_name):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        audio_name = str.join(" ", audio_name)
        print(char_name, audio_name)
        url = get_servertwo(char_name, audio_name)
        file_name = "data/vc." + url.split(".")[-1]
        urllib.request.urlretrieve(url, file_name)
        audio_scr = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=file_name)
        volume_adjusted = discord.PCMVolumeTransformer(audio_scr, volume=float(0.5))
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild.voice_client
        await asyncio.sleep(1.5)
        server.play(volume_adjusted)
        await recursiveTryToLeave(server)
    except AttributeError:
        await ctx.send("Error, cant find the voice line for " + str([char_name, audio_name]))
    except Exception:
        var = traceback.format_exc()
        await ctx.send("Error")
        await ctx.channel.send(str(var))
