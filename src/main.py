from configuration import *
from bot import Bot
import nextcord
from dotenv import load_dotenv
import os, logging

from utils.logger import Logger
from utils.shared_functions import get_cogs


def main():
    # Create the logs folder if it doesn't exist
    if not os.path.exists("logs"):
        os.mkdir("logs")
        
    # Create the nextcord debug logger
    Logger("nextcord", "logs/nextcord.log", level=logging.DEBUG, print_level=100)
    
    # Load the environment variables
    load_dotenv()
    
    # Create the bot
    bot = Bot()
    
    # Get the token from the environment variables
    token = os.getenv("TOKEN")
    if not token:
        bot.logger.critical("No token found in the environment variables, please ensure that you have a .env file in the root directory of the project with a TOKEN variable")
        exit(1)

    # Try to load all the cogs
    for cog in get_cogs():
        try:
            bot.load_extension(cog)
            bot.logger.info("✅ Successfully loaded " + cog)
        except Exception as e:
            bot.logger.info("🟥 Failed to load " + cog)
            bot.logger.error(e)
            bot.logger.exception(e)
    
    # Try to run the bot
    try:
        bot.run(token)
    except nextcord.LoginFailure as e:
        bot.logger.critical("Failed to login, please ensure that the token in the .env file is valid")
        bot.logger.exception(e)
        exit(1)
    
if __name__ == "__main__":
    main()
