import discord
import praw
import keys
from secrets import randbelow, choice

from logger import Log

log = Log("food")

reddit = praw.Reddit(client_id=keys.reddit_id, client_secret=keys.reddit_secret, user_agent='script by u/kattulel')


def is_url_image(image_url):
    ext_list = ["jpg", "jpeg", "png", "gif"]
    ext = str(image_url).rsplit('.', 1)[1]
    return True if ext in ext_list else False


def get_pic():
    posts = []
    subreddit = choice(['FoodPorn', 'pizza', 'burgers', 'DessertPorn', 'eatsandwiches', 'sexypizza', 'food'])

    query = reddit.subreddit(subreddit).hot(limit=100)

    for i in query:
        if is_url_image(i.url):
            posts.append(i)

    result = posts[randbelow(len(posts))]
    log.inline(subreddit, "cyan")

    return result.url


async def food(ctx):
    log.begin("cyan", ctx)
    url = get_pic()
    embed = discord.Embed()
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    log.end()
