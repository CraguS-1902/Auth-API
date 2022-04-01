from random import randint
from os import system

import discord
import MySQLdb
import random
import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
import functions 
# DC
with open("config.json", "r") as read_file:
    data = json.load(read_file)

# Config
TOKEN = data["BotToken"]
GUILD_ID = data["guild_id"]
VERIFY_ROLE_ID = data["verify_role_id"]
mysql = data["MySQL"]
HOST = mysql["host"]
USER = mysql["user"]
PASSWD = mysql["password"]
DB = mysql["database"]

# MYSQL
db = MySQLdb.connect(host=HOST,
                     user=USER,   
                     passwd=PASSWD, 
                     db=DB)      
cur = db.cursor()
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

# Connect Handler

menu = """ █████╗ ██╗   ██╗████████╗██╗  ██╗     █████╗ ██████╗ ██╗
██╔══██╗██║   ██║╚══██╔══╝██║  ██║    ██╔══██╗██╔══██╗██║
███████║██║   ██║   ██║   ███████║    ███████║██████╔╝██║
██╔══██║██║   ██║   ██║   ██╔══██║    ██╔══██║██╔═══╝ ██║
██║  ██║╚██████╔╝   ██║   ██║  ██║    ██║  ██║██║     ██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝     ╚═╝
                                                         """                               
@bot.event
async def on_ready():
    print(functions.fade(menu))
    print(functions.fadea(f'\n{bot.user} has connected to Discord!'))
    guild = bot.get_guild(GUILD_ID)
    print("\n")
    print(functions.fadea(f"Connected with {len(guild.members)} Members"))
# Leave Handler
@bot.event
async def on_member_remove(member):
    functions.log(f"[-] [{member.name}] Leaved the Server.")

# Join Handler
@bot.event
async def on_member_join(member):
    functions.log(f"[+] [{member.name}] Joined the Server.")
    try:
        cur.execute("SELECT * FROM users WHERE discord_id = '" + str(member.id) +"'")
        db.commit()
        key = cur.fetchall()
        for x in key:
            key = x[2]
        embed = discord.Embed(colour=discord.Colour(0x129ecc))

        embed.set_author(name="Auth API | Welcome")
        embed.set_footer(text="Auth API")

        embed.add_field(name="Your key: ``" + key + "``", value="Please don't forget your key")

        await member.send(embed=embed)
    except:

        embed.set_author(name="Auth API | Welcome")
        embed.set_footer(text="Auth API")

        embed.add_field(name="Error", value="Please go to the Website and get the your Key.")

        await member.send(embed=embed)



# Set Key command

@bot.command()
@has_permissions(administrator=True)
async def setkey(ctx, user: discord.Member = None, *, key = None):
    if key is None:
        embed = discord.Embed(colour=discord.Colour(0x129ecc), description=f"**Error, Please enter a Key**")

        embed.set_author(name="Auth Bot")
        embed.set_footer(text="Coded with ❤ by CraguS")

        await ctx.send(embed=embed)
        return
    if user is None:
        embed = discord.Embed(colour=discord.Colour(0x129ecc), description=f"**Error, Please mention a User**")

        embed.set_author(name="Auth Bot")
        embed.set_footer(text="Coded with ❤ by CraguS")

        await ctx.send(embed=embed)
    else:
        
        cur.execute("UPDATE users SET auth_key = '" + key + "' WHERE discord_id = '" + str(user.id) + "'")
        db.commit()
        embed = discord.Embed(colour=discord.Colour(0x129ecc), description=f"**Succussfully, Change Auth Key for **\n<@{user.id}>")
        embed.set_author(name="Auth Bot")
        embed.set_footer(text="Coded with ❤ by CraguS")
        await ctx.message.delete()
        await ctx.send(embed=embed)
        embed = discord.Embed(colour=discord.Colour(0x129ecc))

        embed.set_author(name="Auth API | Your key has been Updated.")
        embed.set_footer(text="Auth API")

        embed.add_field(name="Your key: ``" + key + "``", value="Please don't forget your key")

        await user.send(embed=embed)

# Reset Key
@bot.command()
@has_permissions(administrator=True)
async def resetkey(ctx, user: discord.Member = None):
    if user is None:
        embed = discord.Embed(colour=discord.Colour(0x129ecc), description=f"**Error, Please mention a User**")

        embed.set_author(name="Auth Bot")
        embed.set_footer(text="Coded with ❤ by CraguS")

        await ctx.send(embed=embed)
    else:
        key = random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') + random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')+random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')+random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')+random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')+random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        cur.execute("UPDATE users SET auth_key = '" + key + "' WHERE discord_id = '" + str(user.id) + "'")
        db.commit()
        embed = discord.Embed(colour=discord.Colour(0x129ecc), description=f"**Succussfully, Change Auth Key for **\n<@{user.id}>")
        embed.set_author(name="Auth Bot")
        embed.set_footer(text="Coded with ❤ by CraguS")
        await ctx.message.delete()
        await ctx.send(embed=embed)
        embed = discord.Embed(colour=discord.Colour(0x129ecc))

        embed.set_author(name="Auth API | Your key has been Updated.")
        embed.set_footer(text="Auth API")

        embed.add_field(name="Your key: ``" + key + "``", value="Please don't forget your key")

        await user.send(embed=embed)


# Verify Handler
@bot.listen("on_message")
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel):
        cur.execute("SELECT * FROM users WHERE discord_id = '" + str(message.author.id) +"'")
        db.commit()
        key = cur.fetchall()
        for x in key:
            key = x[2]
        if message.content == key:
            embed = discord.Embed(colour=discord.Colour(0x129ecc))
            guild = bot.get_guild(GUILD_ID)
            role = discord.utils.get(guild.roles,  id=VERIFY_ROLE_ID)

            functions.log(f"[+] [{message.author.name}] got successfully verified.")
            embed.set_author(name="Auth API | Thanks for Verifying")
            embed.set_footer(text="Auth API")
            member = guild.get_member(message.author.id)
            await member.add_roles(role)
            await message.channel.send(embed=embed)

bot.run(TOKEN)