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
from models import Member, Session, engine

# required intents
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# setting up the bot
load_dotenv()
DISCORD_TOKEN = os.environ.get('TOKEN')
client = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(client,sync_commands=True)

# setting up local database session
localSession = Session(bind=engine)

# required guild ids (replace with your guild/server ids)
welcome_channel = 926017686973083679
reaction_channel = 926038951729438730

# helper function to fetch a database entry
def fetch_member(name):
    return localSession.query(Member).filter(Member.name==name).first()


# helper function to insert a new entry
def add_member(name):
    new_member = Member(name=name)
    localSession.add(new_member)
    localSession.commit()

# bot ready message
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

# help command start
client.remove_command('help')
async def help_func(ctx):
    em = discord.Embed(title="Help", description="Here are the list of commands you can use", color=0x00ff00)
    em.add_field(name="/help", value="Shows the help menu", inline=False)
    em.add_field(name="/assign <member> <role>", value="Assign an existing role to a member or create and assign a new one", inline=False)
    em.add_field(name="/register <name>", value="Add a new name to the database", inline=False)
    em.add_field(name="/names", value="Returns all the registered members from the database", inline=False)
    await ctx.send(embed=em)

@client.group(invoke_without_command=True)
async def help(ctx):
    await help_func(ctx)

@slash.slash(name="help", description="Shows the help menu")
async def help(ctx):
    await help_func(ctx)
# help command end

# new member event response
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
    channel = client.get_channel(welcome_channel)
    await channel.send(random.choice(welcome_messages))

# reaction event response (triggered only by reacting with :white_check_mark: emoji)
@client.event
async def on_reaction_add(reaction, user):
    if emoji.demojize(reaction.emoji) == ":check_mark_button:":
        channel = client.get_channel(reaction_channel)
        await channel.send("Reaction added")

# assign role command start
async def assign_func(ctx, member: discord.Member, role):
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
async def assign(ctx, member: discord.Member, role):
    await assign_func(ctx, member, role)

@slash.slash(name='assign', description='Assign an existing role to a member or create and assign a new one')
async def assign_slash(ctx, member: discord.Member, role):
    await assign_func(ctx, member, role)
# assign role command end

# register name command start
async def register_func(ctx, name):
    if fetch_member(name):
        await ctx.send(f'Member named **{name}** already registered. Please use a different name.')
    else:
        add_member(name)
        await ctx.send(f'New member **{name}** succesfully registered!')

@client.command()
async def register(ctx, name):
    await register_func(ctx, name)

@slash.slash(name='register', description='Add a new name to the database')
async def register_slash(ctx, name):
    await register_func(ctx, name)
# register name command end

# names command start
async def names_func(ctx):
    msg = ''
    members = localSession.query(Member).all()
    for member in members:
        name = member.name
        msg = msg + f'\n{name}'
    if msg:
        await ctx.send(f'```{msg}```')
    else:
        await ctx.send("hmm... the database seems empty")

@client.command()
@commands.has_any_role("Moderator", "Admin")
async def names(ctx):
    await names_func(ctx)

@slash.slash(name='names', description='Returns all the registered members from the database')
@commands.has_any_role("Moderator", "Admin")
async def names_slash(ctx):
    await names_func(ctx)
# names command end

# names command error handler
@names.error
async def names_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('welp.. seems like you don\'t have the permission to do that.')

# names_slash command error handler
@names_slash.error
async def names_slash_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('welp.. seems like you don\'t have the permission to do that.')

client.run(DISCORD_TOKEN) # initialize bot
