from tkinter.filedialog import SaveAs
from bs4 import BeautifulSoup
# from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas
import os

def DVFT(los):
    ids = []
    for index, item in enumerate(los):
        vid_id = SVI(item)
        ids += [vid_id]
    print('Downloading Songs')
    DVFI(ids)

def DVFI(lov):
    SAVE_PATH = str(os.pat.join(Path.home(), 'Downloads/songs'))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print('Download folder exists')
    
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
        ydl.download(lov)

def SVI(query):
    print("Getting video id for: ", query)
    BASIC = "http://www.youtube.com/results?search_query="
    URL = (BASIC + query)
    page = requests.get(URL)
    response = requests.get(URL)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, 'html.parser')

    results = soup.find('a', id='video-title')
    return results['href'].split('/watch?v=')

def __main__():
    data = pandas.read_csv('songs.csv')
    data = data['column'].tolist()
    print('Found ', len(data), ' songs')
    DVFT(data[0:1])

__main__()