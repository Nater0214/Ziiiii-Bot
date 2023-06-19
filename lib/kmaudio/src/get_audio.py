# src/get_audio.py
# For getting Kevin audios


# Imports
from selenium import webdriver


# Definitions
def get_audio(query: str):
    """Get a Kevin audio by a search query"""
    
    # Initialize webdriver
    options = webdriver.Chrome.Options()
    for a in {'--log-level=1', '--headless'}: options.add_argument(a)
    driver = webdriver.Chrome(options=options)
    
    # Get the music webpage
    driver.get("https://incompetech.com/music/royalty-free/music.html")