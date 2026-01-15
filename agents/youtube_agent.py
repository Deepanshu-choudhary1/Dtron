import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup

def play_youtube_video(query):
    search_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={search_query}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "/watch?v=" in href:
            video_url = "https://www.youtube.com" + href
            webbrowser.open(video_url)
            return f"Playing {query} on YouTube"

    webbrowser.open(url)
    return f"Searching YouTube for {query}"
