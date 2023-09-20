# This example requires the 'members' and 'message_content' privileged intents to function.

import random
import logging
import logging.handlers

import discord
from discord.ext import commands

token = "put the bot's token here. the bot wont run if its token isn't here."

description = '''this bot has most of its code from https://github.com/Rapptz/discord.py/blob/v2.3.2/examples/basic_bot.py
it also has logging.
'''

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True



bot = commands.Bot(command_prefix='?',
                   description=description,
                   intents=intents,
                  )

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')



@bot.command()
async def add(ctx, left: int, right: int):
  """Adds two numbers together."""
  await ctx.send(left + right)

@bot.command()
async def div(ctx, left: int, right: int):
  """divides two numbers."""
  await ctx.send(left/right)

@bot.command()
async def roll(ctx, dice: str):
  """Rolls a dice in NdN format."""
  try:
    rolls, limit = map(int, dice.split('d'))
  except Exception:
    await ctx.send('Format has to be in NdN!')
    return

  result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
  await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
  """Chooses between multiple choices."""
  await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, *, content='repeating...'):
  """Repeats a message multiple times."""
  for _i in range(times):
    await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
  """Says when a member joined."""
  await ctx.send(
      f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def echo(ctx, *, msg='echoed.'):
  """just echos the message the user adds after the ?echo command."""
  await ctx.send(msg)

@bot.command()
async def cat(ctx):
  await ctx.send('meow :3')
  message = await ctx.send(file=discord.File('cat.jpg'))
  await message.add_reaction('🐈‍⬛')
  
@bot.command()
async def crazy(ctx):
  await ctx.send('GO CRAZY AAAAAAAAAAA')
  await ctx.send(file=discord.File('crazy.gif'))


@bot.command()
async def hello(ctx):
  '''replys to the user who ran the command with a gif saying hello'''
  message = await ctx.send(file=discord.File('hello.gif'))
  await message.add_reaction('👋')


@bot.group()
async def cool(ctx):
  """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
  if ctx.invoked_subcommand is None:
    await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
  """Is the bot cool?"""
  await ctx.send('Yes, the bot is cool.')


@bot.group()
async def cmds(ctx):
  """displays all commands.

  checks for a subcommand, and displays more details on a command (if its availiable.)
  """
  if ctx.invoked_subcommand is None:
    await ctx.send('''Commands:
add, div, roll, choose, repeat, joined, echo, cool, cat, crazy, hello''')


"""all commands below are subcommands for the 'cmds' command, this will be expanded upon in the future when more commands are added."""


@cmds.command(name='add')
async def _add(ctx):
  await ctx.send('''Add:
adds two numbers together.

forrmatted as:
add x y''')

@cmds.command(name='div')
async def _div(ctx):
  await ctx.send('''Div:
divides two number together.

formatted as:
div x y''')

@cmds.command(name='roll')
async def _roll(ctx):
  await ctx.send('''Roll:
rolls dice... yea.

formatted as:
roll Ndn''')


@cmds.command(name='choose')
async def _choose(ctx):
  await ctx.send('''Choose:
randomly selects between multiple choices to (attempt) to settle an argument.
  
formatted as:
choose a b''')


@cmds.command(name='repeat')
async def _repeat(ctx):
  await ctx.send('''Repeat:
repeats a message a user specifies a set number of times.

note: this can be used to mass ping, and can also only repeat messages in bursts of five.

formatted as:

repeat x msg
(where x is any number and msg is what you want repeated)''')


@cmds.command(name='joined')
async def _joined(ctx):
  await ctx.send('''Joined:
see a users join date.

formatted as:
joined @user
(this will ping the user btw, so use sparingly.)''')


@cmds.command(name='echo')
async def _echo(ctx):
  await ctx.send('''Echo:
repeats a message a user specifies once

formatted as:
echo msg
''')


@cmds.command(name='cool')
async def _cool(ctx):
  await ctx.send('''Cool:
checks if the user or if the bot is cool.

formatted as:
cool

or:

cool bot
''')

@cmds.command(name='cat')
async def _cat(ctx):
  await ctx.send('''Cat:
displays an image of a cat and meows.

formatted as:
cat''')

@cmds.command(name='crazy')
async def _crazy(ctx):
  await ctx.send('''Crazy:
displays a gif and goes FUCKING CRAZY.

formatted as:
crazy''')

@cmds.command(name='hello')
async def _hello(ctx):
  await ctx.send('''Hello:
greets the chat with a gif.

formatted as:
hello''')

bot.run(token, log_handler=None)

