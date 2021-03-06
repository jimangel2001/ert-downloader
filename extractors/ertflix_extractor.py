import requests
import re
from bs4 import BeautifulSoup

def obtain_html(url):
    html = requests.get(url).text
    return html

def obtain_title(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('title').text
    title = re.sub(":|/|\||\"", "-", title);
    return title


def obtain_player_url(html):
    soup = BeautifulSoup(html, 'lxml')
    player_iframe = soup.find('iframe')
    player_url = re.split('&', (player_iframe.attrs["src"]))[0]
    return player_url


def obtain_geo(html):
    is_geo = re.search("geo=(.*?)&", html)
    return is_geo


def obtain_stream_url(url, is_geo):
    html = requests.get(url).text
    stream_url = re.split("var HLSLink = '(.*)'", html)[1]
    if("dvrorigingr" not in stream_url and is_geo):
        stream_url = re.sub("dvrorigin", "dvrorigingr", stream_url)
    stream_url = re.sub("/playlist.m3u8", "", stream_url)
    return stream_url


def obtain_chunklist(url):
    chunklist_url = url + "/chunklist.m3u8"
    clean_chunklist = []
    chunklist = requests.get(chunklist_url).text.split('\n')
    for chunk in chunklist:
        if ".ts" in chunk:
            clean_chunklist.append(chunk)
    return (clean_chunklist)


def obtain_data(url):
    html = obtain_html(url)
    title = obtain_title(html)
    player_url = obtain_player_url(html)
    is_geo = obtain_geo(html)
    stream_url = obtain_stream_url(player_url, is_geo)
    return {"title": title, "stream_url": stream_url, "chunklist": obtain_chunklist(stream_url)}
