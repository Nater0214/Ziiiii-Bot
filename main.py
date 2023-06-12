# main.py
# Ziiiii Bot
# Does random stuff in the Ziiiii Server


# Imports
import asyncio

from dotenv import load_dotenv

from src import bot


# Definitions
def main() -> None:
    """Main function"""
    
    load_dotenv()
    
    bot.run()


# Run
if __name__ == "__main__":
    main()
    exit(0)