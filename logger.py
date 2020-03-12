from colorama import Fore, Back, Style
import time
import functools


def colors(color):
    switcher = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "reset": Fore.RESET,
    }
    return switcher.get(color)


class Log:
    def __init__(self, name, prefix="@"):
        self.name = name
        self.prefix = prefix
        self.color = None
        self.start_time = 0

    def begin(self, color, ctx, args=None):
        self.color = colors(color)
        self.start_time = round(time.time() * 1000)
        mesg = self.name
        if args is not None:
            mesg = self.name + str(args) + ":"
        print(self.color, self.prefix, ctx.message.author, mesg, end="")

    def inline(self, text, color=None):
        if color is not None:
            print(colors(color), text, Style.RESET_ALL, end="")
        else:
            print(self.color, text, Style.RESET_ALL, end="")

    def end(self):
        print(self.color+" >", round(time.time() * 1000) - self.start_time, "ms", colors("reset"))


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = round(time.time() * 1000)
        mesg = func.__name__
        print(colors("cyan"), "@", mesg, end="")
        func(*args, **kwargs)
        print(colors("cyan") + " >", round(time.time() * 1000) - start_time, "ms", colors("reset"))
    return wrapper
