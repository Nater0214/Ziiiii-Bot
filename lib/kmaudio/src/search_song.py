# src/get_audio.py
# For getting Kevin audios


# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By


# Definitions
class SearchSong:
    """Holding stuff"""
    
    # Init
    def __init__(self) -> None:
        """Initialize the 'function'"""
        
        # Initialize webdriver
        options = webdriver.chrome.options.Options()
        for a in ['--log-level=1', '--headless']: options.add_argument(a)
        self.driver = webdriver.Chrome(options=options)
    
    def __call__(self, query: str):
        """Get a Kevin audio by a search query"""
        
        # Get the music webpage
        self.driver.get("https://incompetech.com/music/royalty-free/music.html")
        
        # Get search bar element
        search_bar_elem = self.driver.find_element(By.ID, "incompetechSearchSearchText")
        
        # Input the query
        search_bar_elem.send_keys(query)
        
        # Get song list element
        song_elems = self.driver.find_elements(By.CLASS_NAME, "search-result-row")
        
        # Get the song names
        song_names = [elem.find_element(By.TAG_NAME, "b").text for elem in song_elems]
        
        # Return song names
        return song_names

search_song = SearchSong()