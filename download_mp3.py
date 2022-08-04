from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas
import os

def DVFT(los): #DownloadVideosFromTitle
    ids = []
    for index, item in enumerate(los):
        vid_id = SVI(item)
        ids += [vid_id]
    print('Downloading Songs')
    print(ids)
    for i in ids:
        DVFI(i)

def DVFI(lov): #DownloadVideosFromIds
    SAVE_PATH = str(os.path.join(Path.home(), 'Downloads/songs'))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print(':)')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', 
        }],
        'outtmpl' : SAVE_PATH + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        link = 'https://www.youtube.com/watch?v=' + lov
        print(link)
        ydl.download([link])

def SVI(query): #ScrapeVideoID
    print("Getting video id for: ", query)
    BASIC = "http://www.youtube.com/results?search_query="
    URL = (BASIC + query)
    URL.replace(" ", "+")
    page = requests.get(URL)
    session = HTMLSession()
    response = session.get(URL)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, 'html.parser') 

    results = soup.find('a', id='video-title')
    return results['href'].split('/watch?v=')[1]

def __main__():
    data = pandas.read_csv('/Users/ryan/Documents/programming/SpotifyPlaylistToYoutubeToMP3/songs.csv')
    data = data['song_names'].tolist()
    print('Found ', len(data), ' songs')
    DVFT(data[0:30])

__main__()