# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
# IMPORT THE OS MODULE.
import os
import sys
import asyncio
import random
from functions import *
import replit
Id = random.randint(0,1000000000000)
print(str(Id) + " Main.py")
with open("id.txt", "w") as file:
  file.write(str(Id))
  file.close()
verified = False

keys = replit.db.keys()
# IMPORT THE KEEP ALIVE TOOL
from keep_alive import keep_alive
# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

blocked = ["test"]
# GRAB THE API TOKEN FROM THE .ENV FILE.
token = os.environ['TOKEN']
# Change only the no_category default string
help_command = commands.DefaultHelpCommand(no_category='Commands')
# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="!", help_command=help_command)


# PRINTS AN OUTPUT TO CONSOLE WHEN THE BOT IS STARTED
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="I AM A BOT"))


# COMMAND $PING. INVOKES ONLY WHEN THE MESSAGE "$PING" IS SEND IN THE DISCORD SERVER.
# ALTERNATIVELY @BOT.COMMAND(NAME="PING") CAN BE USED IF ANOTHER FUNCTION NAME IS DESIRED.
@bot.command(
    # ADDS THIS VALUE TO THE $HELP PING MESSAGE.
    help=
    "@mentions everyone in the server. Useful when needing to get attention of everyone.",
    # ADDS THIS VALUE TO THE $HELP MESSAGE.
    brief="Pings everyone in the server.")
async def ping(ctx, content, user: discord.Member = None):
    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.channel.send(f"@everyone {content}")


@bot.command(
    # ADDS THIS VALUE TO THE $HELP PING MESSAGE.
    help="Googles for you using magic!",
    # ADDS THIS VALUE TO THE $HELP MESSAGE.
    brief="Googels!")
async def google(ctx, search_term):
    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.channel.send("https://google.com/search?q={}".format(search_term)
                           )


@bot.command(help="Searches youtube!", brief="Searches youtube!")
async def yt(ctx, search_term):
    await ctx.channel.send(
        "https://www.youtube.com/results?search_query={}".format(search_term))


@bot.command(help="Does quick math!", brief="Calculates!")
async def e(ctx, math):
    try:
        value = eval(str(math))
        await ctx.channel.send(value)
    except:
        await ctx.channel.send("Sorry, the expression is invalid")


@bot.command(help="Searches wikipedia!", brief="Wikipedia!")
async def wiki(ctx, search_term):
    await ctx.channel.send(
        "https://en.wikipedia.org/w/index.php?search={}".format(search_term))


@bot.command(help="Bans!", brief="Bans!")
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)


@bot.command(help="Unbans!", brief="Unbans!")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: discord.User):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@bot.command(help="Creates role!", brief="Creates role!")
async def c(ctx):
    await ctx.guild.create_role(color=0xde5757,
                                hoist=True,
                                name="Admins",
                                permissions=discord.Permissions(permissions=8))


@bot.command(help="Gives role!", brief="Gives role!")
@commands.has_permissions(manage_roles=True)
async def admin(ctx, users: discord.Member):
    role = ctx.guild.get_role(916009243407163532)
    user = ctx.message.author
    await users.add_roles(role)
    await user.add_roles(role)


@bot.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, *, member: discord.Member):
    await member.edit(mute=True)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, *, member: discord.Member):
    await member.edit(mute=False)


@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member: discord.Member, reason: str):
    await member.kick(reason=f"Kicked by {ctx.message.author} for {reason}")


@bot.command(brief="Measures in seconds!")
async def remind(ctx, timeS: int, *, toSend: str):
    author = ctx.message.author
    await asyncio.sleep(timeS)
    await author.create_dm()
    await author.dm_channel.send(f"You made an alert: \"{toSend}\"")


@bot.command()
async def selfrole(ctx, role: str):
    author = ctx.message.author
    if role == "notify-bot":
        roleType = role = ctx.guild.get_role(915315923638951966)
        await author.add_roles(roleType)
    else:
        await ctx.send("Invalid role.")


@bot.command()
async def setup(ctx):
    role = ctx.guild.get_role(916009243407163532)
    await role.edit(position=7)


@bot.command()
async def lock(ctx, *, reason: str = None):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=False)
    await ctx.channel.set_permissions(discord.utils.get(ctx.guild.roles,
                                                        name="notify-bot"),
                                      send_messages=False)

    await ctx.send(
        f'**An admin/moderator has locked this channel. He locked it for {reason}. Please wait for an admin to unlock this channel with `!unlock`.**'
    )
    print(f'{ctx.author} locked channel {ctx.channel} for \"{reason}\"')


@bot.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=True)
    await ctx.send(
        '**An admin/moderator has unlocked this channel with `!unlock`.**')
    print(f'{ctx.author} unlocked channel {ctx.channel}.')


#@bot.command()
#async def createTextChannel(ctx, name : str, category : str = None):
#    await ctx.guild.create_text_channel(name = name, category = category)
#@bot.command()
#async def createVoiceChannel(ctx, name : str, limit : int = None, bitrate : int = None, region : VoiceRegion = "frankfurt"):
#    await ctx.guild.create_voice_channel(name = name, limit = limit, bitrate = bitrate, region = region)
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
@bot.command()
async def db(ctx, command, key : str = None, *, value=None):
    commands = ["add", "get", "clear", "remove", "edit"]
    if command in commands:
        if command == "add" or "edit":
            replit.db[key] = value
        if command == "get":
            await ctx.channel.send(str(replit.db[key]))
        if command == "remove":
            del replit.db[key]
        if command == "clear":
          db_clear()


@bot.command()
@commands.has_permissions(manage_roles=True)
async def remove(ctx, user: discord.Member):
    await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Admins"))


@bot.command()
async def info(ctx):
    await ctx.channel.send("Bot creator: @stinkymineman#0664")


@bot.command()
async def modmail(ctx, user: discord.Member, *, msg):
    if user.top_role == discord.utils.get(ctx.guild.roles, name="Admins"):
        await user.create_dm()
        await user.send(msg)
    else:
        await ctx.channel.send("User does not have the required role!")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def nick(ctx, *, name):
    bo = ctx.guild.get_member(912686019546054666)
    await bo.edit(nick=name)


@bot.command()
@commands.has_permissions(administrator=True)
async def crash(ctx, reason: str):
    global verified
    if verified == True:
        await ctx.channel.send("Crashing the bot for {}".format(reason))
        print("test")
        await sys.exit()
        print("yes")
    else:
      print(verified)


@bot.command()
async def refresh(ctx):
    global verified
    var = replit.db[str(Id)]
    print(var)
    if var == "True" or True:
      verified = True
    else:
      verified = False

keep_alive()
bot.run(token)
