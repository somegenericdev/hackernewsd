import base64
import json
import logging
from logging import handlers
import os.path
import tempfile
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import sleep

import backoff
import requests
from functional import seq
from pyquery import PyQuery
import jsonpickle
import win11toast
from stopwatch import Stopwatch

HN_LOGO_B64 ="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"


class HackernewsRateLimitException(Exception):
    pass


class RcFile:
    def __init__(self, _queries):
        self.queries = _queries


class HackerNewsStory:
    def __init__(self, _title, _url, _hackerNewsUrl, _lastSeen):
        self.title = _title
        self.url = _url
        self.hackerNewsUrl = _hackerNewsUrl
        self.lastSeen = _lastSeen

    def __eq__(self, other):
        return self.title == other.title and self.url == other.url and self.hackerNewsUrl == other.hackerNewsUrl

def getLogger():
    log_formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")

    logFile = str(Path.home() / ".hackernewsdlog")

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50 * 1024 * 1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)
    return app_log

def getIconPath():
    iconBytes = base64.b64decode(HN_LOGO_B64)
    tempFolder = os.environ['TEMP']
    iconPath = os.path.join(tempFolder, '__hnicon.png')
    with open(iconPath, 'wb') as iconFile:
        iconFile.write(iconBytes)
    return 'file://' + iconPath

@backoff.on_exception(backoff.fibo, HackernewsRateLimitException)
def processPage(pageNumber):
    html = requests.get(f"https://news.ycombinator.com/news?p={pageNumber}").content.decode('utf-8')
    if(html == "Sorry."):
        raise HackernewsRateLimitException("Rate limit occurred.")
    parser = PyQuery(html)
    hackerNewsUrls = parser("tr > td.subtext > span.subline > span.age > a")
    return seq(parser(".titleline > a")).zip(hackerNewsUrls).map(lambda x: HackerNewsStory(x[0].text, x[0].attrib['href'], "https://news.ycombinator.com/" + x[1].attrib['href'], datetime.now(timezone.utc)))


def readRcFile():
    rcFilePath = Path.home() / ".hackernewsdrc"
    with open(rcFilePath, "r") as rcFile:
        return rcFile.read()


# def notify(story):
#     notification.notify(title="New HackerNews story",
#                         message=story.url,
#                         timeout=10)

def notify(story):
    icon = {
        'src': ICON_PATH,
        'placement': 'appLogoOverride'
    }
    tempFile = tempfile.NamedTemporaryFile(suffix=".pyw", delete=False)
    tempFile.write(f'import webbrowser;webbrowser.open("{story.hackerNewsUrl}")'.encode()) #workaround; the notification wouldnt be clickable after it times out otherwise
    tempFile.close()
    win11toast.notify('New HackerNews story', story.title, on_click=tempFile.name, icon=icon)

def getOldStories():
    storiesDbPath = Path.home() / ".hackernewsddb"
    if os.path.exists(storiesDbPath):
        with open(storiesDbPath, "r") as dbFile:
            return jsonpickle.decode(dbFile.read())
    else:
        return []

def writeOldStories(stories):
    storiesDbPath = Path.home() / ".hackernewsddb"
    with open(storiesDbPath, "w") as dbFile:
        dbFile.write(jsonpickle.encode(stories))


ICON_PATH = getIconPath()
logger = getLogger()

while(True):
    try:
        stopwatch = Stopwatch()
        oldStories = getOldStories()
        rcFile = readRcFile()
        queries = json.loads(rcFile)["queries"]
        allStories = seq.range(1, 30).flat_map(lambda p: processPage(p)).to_list()
        filteredStories = seq(allStories).filter(lambda x: seq(queries).map(lambda q: x.title.lower().find(q.lower()) != -1).any()).to_list()
        diffStories = seq(filteredStories).filter(lambda x: not seq(oldStories).filter(lambda y: y == x).any()).to_list()

        for s in diffStories:
            notify(s)

        writeOldStories(seq(oldStories + diffStories).filter(lambda s: (datetime.now(timezone.utc) - s.lastSeen).days < 7).to_list())

        stopwatch.stop()
        logger.info(f"It took {str(stopwatch)} for a full cycle.")
        sleep(600)
    except Exception as e:
        logger.error(f"Unhandled exception occurred", exc_info=True)
        print(e)

