import gtts
import os

languages = gtts.lang.tts_langs(tld='com')


def getlangs():
    return languages


async def langlist(ctx):
    string = ""
    for key, value in languages.items():
        string = string + key + " = " + value + "\n"

    await ctx.author.send(string)


def checkLanguage(tag):
    for key, value in languages.items():
        if key == tag:
            return True
    return False


def make_audio(text, language):
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")

    speech = gtts.gTTS(text=text, lang=language, slow=False)
    speech.save("audio.mp3")


def make_audio_slow(text, language):
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")

    speech = gtts.gTTS(text=text, lang=language, slow=True)
    speech.save("audio.mp3")
