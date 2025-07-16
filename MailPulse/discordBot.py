import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from ai import mail_summarizer


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

secret_role = "Low demand ladkiyan"

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_member_join(member, message):
    await member.send(f"Welcome to the server {member.name}")
    await message.channel.send(f"welcome jaanu {message.author.mention}")


@bot.event 
async def on_ready():
    print(f"ts pmo ngl, {bot.user.name}")


@bot.command()
async def email(ctx):
    dm_mail = mail_summarizer()
    await ctx.author.send(f"{dm_mail}")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")
    

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

