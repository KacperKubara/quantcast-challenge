""" 
Script to scrape lyrics from the random artist
from the www.lyrics.com website
"""
# Built-in modules
import time 
import random
import re
import urllib.request 
from typing import List

# External modules
from bs4 import BeautifulSoup
import requests 


def response_check(status_code: int) -> None:
    """ 
    Check if the GET requests is correct
    
    Parameters
    ----------
    status_code: int
        status code of the get response

    Returns
    -------
    None
    """ 
    if status_code == 200:
        return
    if status_code == 400:
        raise ValueError(f"Invalid response: {response.status_code}")

def links_get(url: str, element_id: str, keyword: str = None) -> List[str]:
    """ 
    Returns list of href links from the certain HTML element
    
    Parameters
    ----------
    url: str
        url of the website
        
    element_id: str 
        ID tag of the HTML element
    
    keyword: str
        keyword to filter the href link with

    Returns
    -------
    List[str]:
        list of links filtered with the keyword from the
        certain HTML element
    """    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.findAll(element_id)
    links_filtered = []
    for link in links:
        if keyword in link.get('href'):
            links_filtered.append(link.get('href'))
    return links_filtered

def cleanhtml(raw_html) -> List[str]:
    """ 
    Cleans from the HTML tags
    
    Parameters
    ----------
    raw_html: str
        string containing HTML tags

    Returns
    -------
    List[str]:
        clean string without HTML tahs
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
    
def lyrics_get(url: str, element_id: str = "pre") -> List[str]:
    """ 
    Gets raw lyrics from the HTML element
    
    Parameters
    ----------
    url: str
        url of the website
        
    element_id: str 
        ID tag of the HTML element

    Returns
    -------
    List[str]:
        Lyrics from the HTML element
    """    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lyrics = soup.find(element_id)
    return cleanhtml(str(lyrics))


if __name__ == "__main__":
    # Get URLs for top artists
    url = "https://www.lyrics.com/"
    response = requests.get(url + "topartists.php")
    response_check(response.status_code)
    # Get all endpoints to artists
    artists_links = links_get(url + "topartists.php", "a", "artist/")
    # Only one artist so the rhymes are in one style
    artist_random = random.choice(artists_links)
    artist_name = artist_random.split('/')[1]
    print(f"Chosen artist: {artist_name}")
    print(url + artist_random)
    
    # Get all URLs for the lyrics
    response = requests.get(url + artist_random)
    response_check(response.status_code)
    # Get links to all lyrics of the artist
    lyrics_links = links_get(url + artist_random, "a", "lyric/")
    print(f"Example link: {lyrics_links[0]}")

    # Clean lyrics from the HTML tags and save into one txt file
    save_path = "./data/" + artist_name + ".txt"
    with open(save_path, "a", encoding="utf-8") as f:
        for lyrics_link in lyrics_links:
            print(f"Link to lyrics: {lyrics_link}")
            response = requests.get(url + lyrics_link)
            response_check(response.status_code)
            lyrics_clean = lyrics_get(url + lyrics_link, "pre")
            f.write(lyrics_clean)
