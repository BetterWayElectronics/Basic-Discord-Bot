import discord
from discord.ext import commands
import re
from collections import defaultdict
import asyncio
import logging
from aiohttp import ClientConnectorError

# Replace 'your-bot-token' with your actual token (and consider using an environment variable instead)
TOKEN = 'your-bot-token'
CATEGORY_NAME = 'Special Category'  # Replace with the name of your category

intents = discord.Intents.default()
intents.message_content = True  # Make sure this is enabled in the Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)
delete_tracker = defaultdict(int)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    logger.info(f'Bot ID: {bot.user.id}')
    logger.info('------')

def contains_url(message):
    url_pattern = re.compile(r'http[s]?://\S+')
    return bool(url_pattern.search(message))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message is in the specified category
    if message.channel.category and message.channel.category.name == CATEGORY_NAME:
        # Delete the message if it has no attachments and doesn't contain a URL
        if not message.attachments and not contains_url(message.content):
            logger.info(f'Message "{message.content}" from {message.author.name} was deleted in #{message.channel.name}')
            await message.delete()
            delete_tracker[message.author.id] += 1

            warning_message = await message.channel.send(
                f'{message.author.mention}, your message has been deleted because it did not contain an image and a URL.'
            )
            
            # Delete the warning message after 2 minutes
            await asyncio.sleep(120)
            await warning_message.delete()
            
            # If the user has had more than one deletion, assign a "Timeout" role temporarily
            if delete_tracker[message.author.id] > 1:
                timeout_role = discord.utils.get(message.guild.roles, name="Timeout")
                if not timeout_role:
                    timeout_role = await message.guild.create_role(name="Timeout")
                await message.author.add_roles(timeout_role)
                await asyncio.sleep(120)
                await message.author.remove_roles(timeout_role)
                delete_tracker[message.author.id] = 0

    # Ensure other commands are processed
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

async def run_bot():
    try:
        await bot.start(TOKEN)
    except ClientConnectorError:
        # Friendly message instead of a traceback when a connection error occurs.
        logger.error("A connection error occurred: Unable to connect to Discord servers. ")
    except Exception as e:
        # Friendly message for any unexpected error.
        logger.error("An unexpected error occurred: " + str(e))
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(run_bot())
