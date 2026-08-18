"""Discord Bot for Price Tracking
Monitor product prices and send notifications to Discord when prices drop or products are back in stock.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

#bot set up
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Events
@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s):')
    print("Ready to monitor prices and send notifications.")

@bot.event
async def on_message(message):
    """Event triggered when a message is sent in a channel the bot has access to."""
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    await bot.process_commands(message)  # Process commands if any
    
@bot.command(name='ping')
async def ping(ctx):
    """Command to check if the bot is responsive."""
    await ctx.send('Pong!')
    
@bot.command(name='hello')
async def hello(ctx):
    """Command to greet the user."""
    await ctx.send(f'Hello, {ctx.author.mention}!')
    
#run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN is not set in the environment variables.")
    else:
        bot.run(TOKEN)