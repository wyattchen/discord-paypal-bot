import discord
import os
from get_responses import get_response
from dotenv import load_dotenv

conversation_history = {}
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("The bot is ready for use!")
    print("-------------------------")

@client.event
async def hello(message):
    await message.channel.send(f'Hello {message.author}, I am the Paypal bot. Would you like to send a payment to a friend?')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages sent by the bot

    # await message.channel.send(f'Hello {message.author}, I am the Paypal bot. Would you like to send a payment to a friend?')
    user_id = message.author.id
    user_message = message.content

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(conversation_history, user_id, user_message)
        if response == 'None':
            response = f"Hello {message.author}, I am the Paypal bot. Would you like to send a payment to a friend? (Start your messages with '?' for private message)"
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

client.run(TOKEN)