import json
import logging
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import backoff
import bs4
import requests
from feedgen.feed import FeedGenerator
from functional import seq
from stopwatch import Stopwatch

from models import Story, StoryType

class HackernewsRateLimitException(Exception):
    pass


class HackerNewsStoryDto:
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

        return seq(zip(titles, urls, hackerNewsUrls, dates)).map(lambda x: HackerNewsStoryDto(x[0], x[1], x[2], datetime.now(timezone.utc), x[3])).to_list()


    def readRcFile(self):
        rcFilePath = Path.home() / ".hackernewsdrc"
        with open(rcFilePath, "r", encoding="utf-8") as rcFile:
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
        with open(rssFilePath, "w", encoding="utf-8") as rssPath:
            rssPath.write(rss)


    def cleanupOldStories(self):
        Story.delete().where(Story.last_seen < datetime.now(timezone.utc) - timedelta(days=7)).execute()

    def getOldStories(self):
        try:
            all_stories = list(Story.select().where(Story.type == StoryType.Hackernews.value))
            print(all_stories)
            return seq(all_stories).map(lambda s: self.entityToDto(s)).to_list()
        except Exception as e:
            return []

    def entityToDto(self, entity : Story) -> HackerNewsStoryDto:
        return HackerNewsStoryDto(entity.title, entity.url, entity.hnurl, entity.last_seen, entity.posted_date)

    def dtoToEntity(self, dto:HackerNewsStoryDto) -> Story:
        return Story(title=dto.title, url=dto.url,hnurl=dto.hackerNewsUrl, last_seen = dto.lastSeen, posted_date=dto.postedDate, type = StoryType.Hackernews.value)


    def insertNewStories(self, stories):
        for s in stories:
            entity = self.dtoToEntity(s)
            entity.save()

    def scrape(self):
        self.logger = self.getLogger()

        try:
            stopwatch = Stopwatch()
            self.cleanupOldStories()
            oldStories = self.getOldStories()
            rcFile = self.readRcFile()
            queries = json.loads(rcFile)["queries"]
            allCurrentStories = seq.range(1, 30).flat_map(lambda p: self.processPage(p)).to_list()
            filteredStories = seq(allCurrentStories).filter(lambda x: seq(queries).map(lambda q: x.title.lower().find(q.lower()) != -1).any()).to_list()
            diffStories = seq(filteredStories).filter(lambda x: not seq(oldStories).filter(lambda y: y == x).any()).to_list()
            self.insertNewStories(diffStories)

            self.generateRss(self.getOldStories())
            self.generateRss(self.getOldStories(), True)

            stopwatch.stop()
            self.logger.info(f"It took {str(stopwatch)} for a full cycle.")
        except Exception as e:
            self.logger.error(f"Unhandled exception occurred", exc_info=True)
            print(e)