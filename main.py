import os
import random
import discord
import emoji
import sqlite3
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord_slash import SlashCommand
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

load_dotenv()
DISCORD_TOKEN = os.environ.get('TOKEN')
client = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(client,sync_commands=True)
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute("""CREATE TABLE members (
            name text
            )""")

def fetch_member(name):
    c.execute("SELECT * FROM members WHERE name=:name", {'name':name})
    return c.fetchone()

def add_member(name):
    with conn:
        c.execute("INSERT INTO members VALUES (:name)", {'name':name})

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):
    welcome_messages = [
    f'Welcome {member.mention}. Say hi!',
    f'Yaay you made it, {member.mention}.',
    f'A wild {member.mention} appeared.',
    f'Everyone welcome {member.mention}!',
    f'Good to see you {member.mention}.',
    f'{member.mention} joined the party.',
    f'Welcome {member.mention}, we hope you brought a pizza.',
    f'{member.mention} hopped into the server.',
    f'{member.mention} just slid into the server.'
    ]
    channel = client.get_channel(926017686973083679)
    await channel.send(random.choice(welcome_messages))

@client.event
async def on_reaction_add(reaction, user):
    if emoji.demojize(reaction.emoji) == ":check_mark_button:":
        channel = client.get_channel(926038951729438730)
        await channel.send("Reaction added")

@client.command()
async def assign(ctx, member: discord.Member, role):
    if get(ctx.guild.roles, name=role):
        var = get(ctx.guild.roles, name=role)
        await member.add_roles(var)
        await ctx.send(f'The role **{role}** was given to **{member.mention}**')
    else:
        guild = ctx.guild
        await guild.create_role(name=role)
        var = get(ctx.guild.roles, name=role)
        await member.add_roles(var)
        await ctx.send(f'The role **{role}** was given to {member.mention}')

@client.command()
async def register(ctx, name):
    if fetch_member(name):
        await ctx.send(f'Member named **{name}** already registered. Please use a different name.')
    else:
        add_member(name)
        await ctx.send(f'New member **{name}** succesfully registered!')

@client.command()
@commands.has_any_role("Moderator", "Admin")
async def names(ctx):
    names = ['John Doe', 'Jane Doe']
    msg = ''
    c.execute("SELECT * FROM members")
    value = c.fetchone()
    while value:
        name = value[0]
        names.append(name)
        value = c.fetchone()
    for name in names:
        msg = msg + f'\n{name}'
    await ctx.send(f'```{msg}```')

@names.error
async def names_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('welp.. seems like you don\'t have the permission to do that.')

client.run(DISCORD_TOKEN)
conn.close()