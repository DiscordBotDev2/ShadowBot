# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
# IMPORT THE OS MODULE.
import os
import subprocess
import sys
import asyncio
import random
import functions
import replit
logging = False
# TODO #
"""
- Error Handling!
- Add better responses to old commands
- Fix SLOWMODE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
# Maybe implement (In order of difficulty; low to high) #
"""
- Rewrite in a active library (slash commands support)?
- Make a website?
- Web dashboard?
"""
Id = random.randint(0, 1000000000000)
print(str(Id) + " Main.py")
with open("id.txt", "w") as file:
    file.write(str(Id))
    file.close()
verified = False
msg = ""
teams = []
giveaways = []
log = []
cat = None
count = 0
category = ""
keys = replit.db.keys()
# IMPORT THE KEEP ALIVE TOOL
from keep_alive import keep_alive
# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

blocked = []
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

@bot.event
async def on_message(message):
    for i in range(0, len(blocked)):
        if blocked[i] in message.content:
            await message.delete()
    await bot.process_commands(message)


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


@bot.group()
async def db(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid database command passed...')


@db.command()
async def add(ctx, key: str, value: str):
    replit.db[key] = value


@db.command()
async def get(ctx, key: str):
    await ctx.channel.send(str(replit.db[key]))


@db.command()
async def remove(ctx, key: str):
    del replit.db[key]


@db.command()
async def clear(ctx):
    functions.db_clear()


@bot.command()
@commands.has_permissions(manage_roles=True)
async def remove(ctx, user: discord.Member):
    await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Admins"))


@bot.command()
async def info(ctx):
    creator = discord.utils.get(ctx.guild.members, name = "stinkymineman#0664")
    print(creator)
    if creator != None:
      await ctx.send(creator.mention)
    else:
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
        print("Crashed. Printing reason...")
        print(reason)
        await sys.exit()
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


@bot.command()
async def slowmode(ctx, delay: int, *, channel: str = None):
    if channel == None:
        await ctx.channel.edit(slowmode_delay=delay)
    else:
        channel = discord.utils.get(ctx.guild.text_channels, name=channel)
        await channel.edit(slowmode_delay=delay)


@bot.group()
async def giveaway(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid giveaway command passed...')


@giveaway.command()
async def start(ctx, *, name: str):
    global msg
    msg = await ctx.channel.send(name)
    await msg.add_reaction("🔑")


@giveaway.command()
async def end(ctx):
    global msg
    users = msg.reactions[0].users().flatten()
    await ctx.channel.send(random.choice(users))


@bot.group()
async def bash(ctx):
    if ctx.invoked_subcommand == None:
        await ctx.send("Invalid shell command!")


@bash.command()
async def make_shell(ctx):
    await ctx.send("Initializing a shell...")
    if verified == True:
        subprocess.run(["mkdir", "./users/" + ctx.message.author.name])
    else:
        await ctx.send("You dont have the correct perms!")


@bash.group(aliases = ["$"])
async def run(ctx):
    if ctx.invoked_subcommand == None:
        await ctx.send("Invalid function. |!help bash $| for more")
    else:
        with open("./users/" + ctx.message.author.name + "/history.bash",
                  "a") as f:
            f.write(ctx.invoked_subcommand.name + "\n")
            f.close()


@run.command()
async def test(ctx):
    await ctx.send("Test complete!")


@run.command()
async def history(ctx):
    with open("./users/" + ctx.message.author.name + "/history.bash",
              "r") as f:
        data = f.readlines()
        await ctx.send(functions.unbackslash(data))
        f.close()


@bot.command()
async def unverify(ctx):
    global Id
    global verified
    verified = False
    replit.db[Id] = False
    Id = "403 - Forbidden"

@bot.group(aliases = ["tm"])
async def tournament(ctx):
  if ctx.invoked_subcommand == None:
    await ctx.send("Wrong tournament command!")

@tournament.command()
async def start(ctx, teams_count : int, members_in_team : int, *, game : str):
  global cat
  global teams
  if cat != None:
    await ctx.send("There is already a tournament running!")
  else:
    cat = await ctx.guild.create_category("Tournament : " + game)
    for i in range(1,teams_count + 1):
      teams.append(await ctx.guild.create_voice_channel("team_" + str(i), user_limit = members_in_team + 2, category = cat))

@tournament.command(aliases = ["end"])
async def stop(ctx):
  await cat.delete()
  for i in range(0,len(teams)):
    await teams[i].delete()

@bot.group(invoke_without_subcommand = True)
async def automod(ctx):
  await ctx.send("Invalid subcommand!")

@automod.command()
async def add(ctx, term : str):
  blocked.append(term)
@automod.command()
async def remove(ctx, term : str):
  try:
    blocked.remove(term)
  except ValueError:
    ctx.send("Term does not exist!")

@bot.command()
async def warn(ctx, user : discord.Member):
  if user == ctx.guild.owner:
    if not os.path.isdir("./users/" + user.name):
      subprocess.run(["mkdir", "./users/" + user.name])
    if os.path.isfile("./users/" + user.name + "/warn"):
      await ctx.send("The users has already been warned, banning instead...")
      await user.ban()
    else:
      subprocess.run(["touch", "./users/" + user.name + "/warn"])
      await ctx.send("The user has been warned!")
  else:
    await ctx.send("really.")
keep_alive()
bot.run(token)
