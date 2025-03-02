import base64
import json
import logging
import re
import os.path
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import backoff
import bs4
import requests
from feedgen.feed import FeedGenerator
from functional import seq
from pyquery import PyQuery
import jsonpickle
from stopwatch import Stopwatch

HN_LOGO_B64 ="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"


class HackernewsRateLimitException(Exception):
    pass


class RcFile:
    def __init__(self, _queries):
        self.queries = _queries


class HackerNewsStory:
    def __init__(self, _title, _url, _hackerNewsUrl, _lastSeen, _postedDate):
        self.title = _title
        self.url = _url
        self.hackerNewsUrl = _hackerNewsUrl
        self.lastSeen = _lastSeen
        self.postedDate = _postedDate

    def __eq__(self, other):
        return self.url == other.url and self.postedDate == other.postedDate

class HackerNewsScraper():
    def __init__(self):
        pass

    def getLogger(self):
        rootLogger = logging.getLogger('root')
        return rootLogger

    def getIconPath(self):
        iconBytes = base64.b64decode(HN_LOGO_B64)
        tempFolder = tempfile.gettempdir()
        iconPath = os.path.join(tempFolder, '__hnicon.png')
        with open(iconPath, 'wb') as iconFile:
            iconFile.write(iconBytes)
        return 'file://' + iconPath

    @backoff.on_exception(backoff.fibo, HackernewsRateLimitException)
    def processPage(self, pageNumber):
        self.logger.info(f"Getting page {pageNumber}")

        resp = requests.get(f"https://news.ycombinator.com/news?p={pageNumber}", timeout=30)
        html = resp.content.decode('utf-8')
        if(resp.status_code == 503 or html == "Sorry."):
            self.logger.info("Rate limited. Retrying.")
            raise HackernewsRateLimitException("Rate limit occurred.")

        parser = bs4.BeautifulSoup(html, features="lxml")
        hackerNewsUrls = seq(parser.select("span.age > a")).map(lambda x: "https://news.ycombinator.com/" + x['href']).to_list()
        titles = seq(parser.select(".titleline > a")).map(lambda x: x.text).to_list()
        urls = seq(parser.select(".titleline > a")).map(lambda x: x['href']).map(lambda x: "https://news.ycombinator.com/" + x if x.startswith("item?id") else x).to_list()

        dates = seq(parser.select("span.age")).map(lambda x: x['title']).map(lambda x: datetime.fromtimestamp(int(re.findall(r"[0-9]{10,}", x)[0]), timezone.utc)).to_list()

        if not (len(hackerNewsUrls) == len(titles) == len(urls) == len(dates)):
            raise Exception(f"Error in parsing page {pageNumber}: length of parsed elements is different. Hackernewsurls: {len(hackerNewsUrls)} Titles: {len(titles)} Urls: {len(urls)} Dates: {len(dates)}\n\n#Hackernewsurls\n{hackerNewsUrls}\n\n#Titles\n{titles}\n\n#Urls\n{urls}\n\n#Dates\n{dates}")

        return seq(zip(titles, urls, hackerNewsUrls, dates)).map(lambda x: HackerNewsStory(x[0], x[1], x[2], datetime.now(timezone.utc), x[3])).to_list()


    def readRcFile(self):
        rcFilePath = Path.home() / ".hackernewsdrc"
        with open(rcFilePath, "r") as rcFile:
            return rcFile.read()




    def generateRss(self, stories, useHackernewsUrl=False):
        fg = FeedGenerator()
        fg.title('Hackernewsd - HN' if useHackernewsUrl else 'Hackernewsd - Blog')
        fg.link(href='http://localhost:5555', rel='alternate')  #TODO parameterize
        # fg.logo('http://ex.com/logo.jpg')
        fg.subtitle('Hackernewsd - HN' if useHackernewsUrl else 'Hackernewsd - Blog')
        fg.language('en')
        for story in stories:
            fe = fg.add_entry()
            fe.title(story.title)
            fe.published(story.postedDate)
            fe.link(href=story.hackerNewsUrl if useHackernewsUrl else story.url)

        rss = fg.rss_str(pretty=True).decode('utf-8')
        rssFilePath = Path.home() / ".hackernewsdrss_hn" if useHackernewsUrl else Path.home() / ".hackernewsdrss"
        with open(rssFilePath, "w") as rssPath:
            rssPath.write(rss)


    def getOldStories(self):
        storiesDbPath = Path.home() / ".hackernewsddb"
        if os.path.exists(storiesDbPath):
            with open(storiesDbPath, "r") as dbFile:
                return jsonpickle.decode(dbFile.read())
        else:
            return []

    def writeOldStories(self, stories):
        storiesDbPath = Path.home() / ".hackernewsddb"
        with open(storiesDbPath, "w") as dbFile:
            dbFile.write(jsonpickle.encode(stories))

    def scrape(self):
        self.ICON_PATH = self.getIconPath()
        self.logger = self.getLogger()

        try:
            stopwatch = Stopwatch()
            oldStories = self.getOldStories()
            rcFile = self.readRcFile()
            queries = json.loads(rcFile)["queries"]
            allStories = seq.range(1, 30).flat_map(lambda p: self.processPage(p)).to_list()
            filteredStories = seq(allStories).filter(lambda x: seq(queries).map(lambda q: x.title.lower().find(q.lower()) != -1).any()).to_list()
            diffStories = seq(filteredStories).filter(lambda x: not seq(oldStories).filter(lambda y: y == x).any()).to_list()


            updatedOldStories = seq(oldStories + diffStories).filter(lambda s: (datetime.now(timezone.utc) - s.lastSeen).days < 7).to_list()
            self.writeOldStories(updatedOldStories)
            self.generateRss(updatedOldStories)
            self.generateRss(updatedOldStories, True)

            stopwatch.stop()
            self.logger.info(f"It took {str(stopwatch)} for a full cycle.")
        except Exception as e:
            self.logger.error(f"Unhandled exception occurred", exc_info=True)
            print(e)
