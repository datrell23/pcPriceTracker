"""Discord Bot for Price Tracking
Monitor product prices and send notifications to Discord when prices drop or products are back in stock.
"""

import discord
from discord.ext import commands, tasks
import os
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables from
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID', 0)


#bot set up
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Helpers
def load_latest_price():
    """Load the latest price from price_history"""
    try:
        with open('price_history.json', 'r') as f:
            data = json.load(f)
            if data:
                return data[-1] # Last entry in the price history
            return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def build_price_embed(latest, title, color):
    """Build a price embded sop commands and auto-posy look the same."""
    embed = discord.Embed(title='Current Price', color=discord.Color.green())
    embed.add_field(name='Product', value=latest['product'], inline=False)
    embed.add_field(name='Price', value=f"${latest['price']}", inline=True)
    embed.add_field(name='Stock Status', value=latest['stock_status'], inline= True)
    embed.add_field(name='Last Checked', value=latest['timestamp'], inline=False)
    embed.add_field(name='URL', value=f"[View on Newegg]({latest['url']})", inline=False)
    return embed

# Backgroudn Task
@tasks.loop(minutes=1)
async def auto_post_price():
    """Post the latest price to the specified Discord channel."""
    print(f"[{datetime.now()}] Runnind auot price update...")
    
    latest = load_latest_price()
    if not latest:
        print("No price data available")
        return
    channel = bot.get_channel(int(CHANNEL_ID))
    if not channel:
        print("Channel not found - check DISCORD_CHANNEL_ID in .env")
        return
    embed = build_price_embed(latest, 'Current Price', discord.Color.blue())
    await channel.send(embed=embed)
    print("Price posted to Discord") 
    
#Events 
@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s):')
    if not auto_post_price.is_running():
        auto_post_price.start()
    
@bot.event
async def on_message(message):
    """Event triggered when a message is sent in a channel the bot has access to."""
    if message.author == bot.user:
        return  
    await bot.process_commands(message)  
    
#Commands
@bot.command(name='ping')
async def ping(ctx):
    """Command to check if the bot is responsive."""
    await ctx.send('Pong!')
    
@bot.command(name='hello')
async def hello(ctx):
    """Command to greet the user."""
    await ctx.send(f'Hello, {ctx.author.mention}!')
    
@bot.command(name='price')
async def price(ctx):
    """Display the latest price"""
    latest = load_latest_price()
    if not latest:
        await ctx.send('No price history available. Run Scraper!')
        return 
    await ctx.send(embed=embed)
    
#run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN is not set in the environment variables.")
    else:
        bot.run(TOKEN)