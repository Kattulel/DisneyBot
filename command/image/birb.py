import discord
import requests
from logger import Log

log = Log("birb")


async def birb(ctx):
	log.begin("cyan", ctx)
	r = requests.get('http://random.birb.pw/tweet/')
	url = "https://random.birb.pw/img/" + str(r.text)
	embed = discord.Embed()
	embed.set_image(url=url)
	await ctx.send(embed=embed)
	log.end()
