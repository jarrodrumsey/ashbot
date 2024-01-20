import os
import discord
from dotenv import load_dotenv
from bot import BotClient;

# Load the .env file
load_dotenv();
TOKEN = os.getenv('DISCORD_TOKEN')

# Create a client instance of the bot
client = BotClient();

# Run the bot with the token
client.run(TOKEN);