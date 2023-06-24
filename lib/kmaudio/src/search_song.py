# src/get_audio.py
# For getting Kevin audios


# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Definitions
class SearchSong:
    """Holding stuff"""
    
    # Init
    def __init__(self) -> None:
        """Initialize the 'function'"""
        
        # Initialize webdriver
        options = webdriver.ChromeOptions()
        for a in ["--no-sandbox", "--headless=new", "--disable-gpu", "--window-size=1920,1080"]: options.add_argument(a)
        self.driver = webdriver.Chrome(options=options)
    
    def __call__(self, query: str, download=False):
        """Get a Kevin audio by a search query"""
        
        # Get the music webpage
        self.driver.get("https://incompetech.com/music/royalty-free/music.html")
        
        # Refresh the page
        self.driver.refresh()
        
        # Get search bar element
        search_bar_elem = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(By.ID, "incompetechSearchSearchText"))
        
        # Input the query
        search_bar_elem.send_keys(query)
        
        # Get song list element
        song_elems = self.driver.find_elements(By.CLASS_NAME, "search-result-row")
        
        # Get the song names
        song_names = [elem.find_element(By.TAG_NAME, "b").text for elem in song_elems]
        
        if download:
            # Download the song
            # Ensure song is found
            if query not in song_names:
                raise ValueError("Song not found")
            
            # Get the song element
            for elem in song_elems:
                if elem.find_element(By.TAG_NAME, "b").text == query:
                    song_elem = elem
                    break
            
            # Click the song element
            song_elem.click()
            
            # Get the download button
            download_button = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/div/div[1]/a[1]")
            
            # Return the song link
            return download_button.get_attribute('href')
            
        else:
            # Return song names
            return song_names

search_song = SearchSong()