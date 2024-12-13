import discord
import logging
import logging.handlers
import datetime
import test_image

with open('TOKEN.txt') as f:
    DISCORD_TOKEN = f.read()

enable_logging = True

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

emotions = ['🇱', '🇮', '🇳', '🇰',
            '❔']

if enable_logging:
    # Configure the logger
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    # Create a file handler and set the log file path
    handler = logging.handlers.RotatingFileHandler(
        filename='logs/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_bot.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Function to process attached images
async def process_images(images):
    for image in images:
        if image.content_type.startswith('image/'):
            # Read the image attachment
            image_bytes = await image.read()
            if test_image.check_for_raidbots(image_bytes):
                return True


# Function to check if the message text contains a specific website link
def contains_link(content):
    return "www.raidbots.com" in content


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # Check if the message has attachments
    if len(message.attachments) > 0:

        if enable_logging:
            # Log the server, channel, and user information
            logger.info(f'CHECK | Server: {message.guild.name} | Channel: {message.channel.name} | User: {message.author.name}')

        # Check if the message text contains the raidbots link
        if not contains_link(message.content):
            if await process_images(message.attachments):
                response_message = f"{message.author.mention} стоит скинуть ссылку на сим, а не скриншот. Спасибо!"

                if enable_logging:
                    # Log the server, channel, and user information
                    logger.info(
                        f'TRIGGERED | Server: {message.guild.name} | Channel: {message.channel.name} | User: {message.author.name}')

                for emotion in emotions:
                    await message.add_reaction(emotion)
                await message.channel.send(response_message)


bot.run(DISCORD_TOKEN, log_handler=None)
