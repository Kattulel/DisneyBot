
async def button_onClick(reaction, voice_client):
    if voice_client is not None:
        if voice_client.is_paused():
            if reaction.emoji == "\U000025B6":  # resume
                await resume(voice_client)

        if voice_client.is_playing():
            if reaction.emoji == "\U000023F8":  # pause
                await pause(voice_client)

        if reaction.emoji == "\U000023F9":  # stop
            if voice_client.is_playing():
                await stop(voice_client)

            message = reaction.message
            if message.author.bot:
                await message.delete()


async def addmenu(message):
    playbtn = "\U000025B6"
    pausebtn = "\U000023F8"
    stopbtn = "\U000023F9"
    await message.add_reaction(playbtn)
    await message.add_reaction(pausebtn)
    await message.add_reaction(stopbtn)


async def genMusicMenu(ctx, video_title):
    import discord.embeds
    user = str(ctx.author)

    embed = (discord.Embed(title='\U0001F3B5 Now playing',
                           description=video_title,
                           color=discord.Color.blue())
             .set_footer(text="Requested by: " + user))

    menu = await ctx.send(embed=embed)
    await addmenu(menu)


async def pause(vc):
    await vc.pause()


async def resume(vc):
    await vc.resume()


async def stop(vc):
    await vc.disconnect()
