import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import shelve
from random import randint

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    outlet = bot.get_channel(1084263687138852879)
    await outlet.send(f"We have logged in as {bot.user}")


async def is_jack(ctx: commands.Context):
    return ctx.author.id == 281901487830073345


@bot.command(name="andrew")
@commands.check(is_jack)
async def andrew(ctx: commands.Context):
    db = shelve.open("usernames.db")
    await ctx.send("Changing names")
    guild = bot.get_guild(1084263687138852874)
    with open("andrews.txt") as f:
        andrews = f.readlines()
        andrew_len = len(andrews)
    for count, member in enumerate(guild.members):
        if count % 20 == 0:
            try:
                await ctx.send(f"Changed {count} of {guild.member_count}")
            except Exception as e:
                print("Failed to update progress with {e}")
                await ctx.send("Failed to update progress with {e}")
        try:
            db[f"{count}"] = {"old_name": member.display_name, "userID": member.id}
            await member.edit(nick=andrews[randint(0, andrew_len)])
        except Exception as e:
            print(f"Failed to change name of member {member.display_name}:{member.id} with error: {e}")
            await ctx.send(f"Failed to change name of member {member.display_name}:{member.id} with error: {e}")
    await ctx.send("Finished changing names")


@bot.command(name="change_back")
@commands.check(is_jack)
async def change_back(ctx: commands.Context):
    db = shelve.open("usernames.db")
    await ctx.send("Changing names back")
    guild = bot.get_guild(1084263687138852874)

    db_list = list(db.items())

    for count, item in db_list:
        if int(count) % 20 == 0:
            try:
                await ctx.send(f"Changed {count} of {guild.member_count}")
            except:
                print("Failed to update progress with {e}")
                await ctx.send("Failed to update progress with {e}")
        try:
            await guild.get_member(item["userID"]).edit(nick=item["old_name"])
        except Exception as e:
            print(f"Failed to change name of member {item['old_name']}:{item['userID']} with error: {e}")
            await ctx.send(f"Failed to change name of member {item['old_name']}:{item['userID']} with error: {e}")
    await ctx.send("Finished changing names")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        pass
    print(message.content)
    await bot.process_commands(message)


load_dotenv()
bot.run(os.getenv('TOKEN'))
