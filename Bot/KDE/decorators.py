from discord.ext import commands
""" Todo
    - decorators:
    1: Decorators for permissions"""


def asdf(func):
    def f(*args, **kwargs):
        rv = func(*args, **kwargs)
        print(rv)
        return rv
    return f


def deco():
    def predicate(ctx):
        print(ctx.message.author)
        return True
    return commands.check(predicate)
