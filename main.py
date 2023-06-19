# main.py
# Ziiiii Bot
# Does random stuff in the Ziiiii Server


# Imports
import signal
import sys

from dotenv import load_dotenv

from src import bot


# Definitions
def main() -> None:
    """Main function"""
    
    load_dotenv()
    
    bot.run()


def exit_script() -> None:
    """Exit script"""
    
    sys.exit(0)


# Run
if __name__ == "__main__":
    # Add kill signals
    signal.signal(signal.SIGINT, exit_script)
    signal.signal(signal.SIGTERM, exit_script)
    
    main()
    exit(0)