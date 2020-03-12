from secrets import randbelow
import discord
import praw
import keys
from logger import Log

log = Log("reddit")
ext_list = ["jpg", "jpeg", "png", "gif"]

reddit_s = praw.Reddit(client_id=keys.reddit_id,
                       client_secret=keys.reddit_secret,
                       user_agent='script by u/kattulel')


def is_url_image(image_url):
    ext = str(image_url).rsplit('.', 1)[1]
    return True if ext in ext_list else False


def search_reddit(subreddit, keywords=None):
    posts = []
    query = reddit_s.subreddit(subreddit)

    if keywords is not None:
        query = query.search(keywords, limit=100)
    else:
        query = query.hot(limit=100)

    for i in query:
        if is_url_image(i.url):
            posts.append(i)

    result = posts[randbelow(len(posts))]
    log.inline(result.url, "cyan")
    return result


async def reddit(ctx, subreddit, keywords=None):
    log.begin("cyan", ctx, (subreddit, keywords))
    try:
        result = search_reddit(subreddit, keywords)
        embed = discord.Embed()
        embed.set_image(url=result.url)
        embed.description = "https://www.reddit.com/r/"+subreddit+"/comments/"+result.id
        await ctx.send(embed=embed)
    except IndexError:
        await ctx.send("No Results")
    log.end()
