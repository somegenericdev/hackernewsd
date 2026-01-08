import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from ssl import SSLError
import backoff
import requests
from feedgen.feed import FeedGenerator
from functional import seq
from stopwatch import Stopwatch
from models import Story, StoryType
from types import SimpleNamespace
from dtos import RateLimitException, StoryDto
from concurrent.futures import ThreadPoolExecutor, as_completed


class HackerNewsScraper():
    def __init__(self):
        pass

    def get_logger(self):
        rootLogger = logging.getLogger('root')
        return rootLogger

    @backoff.on_exception(backoff.fibo, SSLError)
    def get_stories(self) -> list[StoryDto]:
        self.logger.info("Getting Hackernews' top stories")
        resp = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=30)

        json_res = resp.content.decode('utf-8')
        story_ids = json.loads(json_res, object_hook=lambda d: SimpleNamespace(**d))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.get_story, story_id) for story_id in story_ids]
            results = []
            for future in as_completed(futures):
                results.append(future.result())
            return results




    @backoff.on_exception(backoff.fibo, SSLError)
    def get_story(self, storyId) -> StoryDto:
        self.logger.info(f"Getting Hackernews story #{storyId}")
        resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{storyId}.json", timeout=30)
        json_res = resp.content.decode('utf-8')
        json_obj = json.loads(json_res, object_hook=lambda d: SimpleNamespace(**d))
        url = getattr(json_obj, "url", None)
        return StoryDto(json_obj.title, None if url == "" else url, f"https://news.ycombinator.com/item?id={json_obj.id}", datetime.now(timezone.utc), datetime.fromtimestamp(json_obj.time, timezone.utc))

    def read_rc_file(self):
        rc_file_path = Path.home() / ".hackernewsdrc"
        with open(rc_file_path, "r", encoding="utf-8") as rc_file:
            return rc_file.read()

    def generate_rss(self, stories, use_hackernews_url=False):
        fg = FeedGenerator()
        fg.title('Hackernewsd - HN' if use_hackernews_url else 'Hackernewsd - HN (Blog)')
        fg.link(href='http://localhost:5555', rel='alternate')  # TODO parameterize
        # fg.logo('http://ex.com/logo.jpg')
        fg.subtitle('Hackernewsd - HN' if use_hackernews_url else 'Hackernewsd - HN (Blog)')
        fg.language('en')
        for story in stories:
            if not use_hackernews_url and story.url == None:
                continue

            fe = fg.add_entry()
            fe.title(story.title)
            fe.published(story.posted_date)
            fe.link(href=story.hacker_news_url if use_hackernews_url else story.url)

        rss = fg.rss_str(pretty=True).decode('utf-8')
        rss_file_path = Path.home() / ".hackernewsdrss_hn" if use_hackernews_url else Path.home() / ".hackernewsdrss_hn_blog"
        with open(rss_file_path, "w", encoding="utf-8") as rss_path:
            rss_path.write(rss)

    def cleanup_old_stories(self):
        Story.delete().where(Story.last_seen < datetime.now(timezone.utc) - timedelta(days=7)).execute()

    def get_old_stories(self):
        try:
            all_stories = list(Story.select().where(Story.type == StoryType.Hackernews.value))
            print(all_stories)
            return seq(all_stories).map(lambda s: self.entity_to_dto(s)).to_list()
        except Exception as e:
            return []

    def entity_to_dto(self, entity: Story) -> StoryDto:
        return StoryDto(entity.title, entity.url, entity.hnurl, datetime.fromisoformat(entity.last_seen).astimezone(timezone.utc), datetime.fromisoformat(entity.posted_date).astimezone(timezone.utc))

    def dto_to_entity(self, dto: StoryDto) -> Story:
        return Story(title=dto.title, url=dto.url, hnurl=dto.hacker_news_url, last_seen=dto.last_seen, posted_date=dto.posted_date, type=StoryType.Hackernews.value)

    def insert_new_stories(self, stories):
        for s in stories:
            entity = self.dto_to_entity(s)
            entity.save()

    def update_last_seen_dates(self, current_stories: list[StoryDto]):
        for story in current_stories:
            Story.update(last_seen=datetime.now(timezone.utc)).where((Story.type == StoryType.Hackernews.value) & (Story.hnurl == story.hacker_news_url) & (Story.posted_date == story.posted_date)).execute()

    def scrape(self):
        self.logger = self.get_logger()

        try:
            stopwatch = Stopwatch()
            self.cleanup_old_stories()
            old_stories = self.get_old_stories()
            rc_file = self.read_rc_file()
            queries = json.loads(rc_file)["queries"]
            all_current_stories = self.get_stories()
            self.update_last_seen_dates(all_current_stories)
            filtered_stories = seq(all_current_stories).filter(lambda x: seq(queries).map(lambda q: x.title.lower().find(q.lower()) != -1).any()).to_list()
            diff_stories = seq(filtered_stories).filter(lambda x: not seq(old_stories).filter(lambda y: y == x).any()).to_list()
            self.insert_new_stories(diff_stories)

            self.generate_rss(self.get_old_stories())
            self.generate_rss(self.get_old_stories(), True)

            stopwatch.stop()
            self.logger.info(f"It took {str(stopwatch)} for a full cycle for Hackernews.")
        except Exception as e:
            self.logger.error(f"Unhandled exception occurred", exc_info=True)
            print(e)


class LobstersScraper():
    def __init__(self):
        pass

    def get_logger(self):
        root_logger = logging.getLogger('root')
        return root_logger

    @backoff.on_exception(backoff.fibo, RateLimitException)
    def process_page(self, page_number) -> list[StoryDto]:
        self.logger.info(f"Getting page {page_number}")

        resp = requests.get(f"https://lobste.rs/page/{page_number}.json", timeout=30)
        if (resp.status_code == 429):
            self.logger.info("Rate limited. Retrying.")
            raise RateLimitException("Rate limit occurred.")

        json_res = resp.content.decode('utf-8')

        json_obj = json.loads(json_res, object_hook=lambda d: SimpleNamespace(**d))
        return seq(json_obj).map(lambda s: StoryDto(s.title, s.url, s.comments_url, datetime.now(timezone.utc), datetime.fromisoformat(s.created_at).astimezone(timezone.utc))).to_list()

    def read_rc_file(self):
        rc_file_path = Path.home() / ".hackernewsdrc"
        with open(rc_file_path, "r", encoding="utf-8") as rc_file:
            return rc_file.read()

    def generate_rss(self, stories, use_hackernews_url=False):
        fg = FeedGenerator()
        fg.title('Hackernewsd - Lobsters' if use_hackernews_url else 'Hackernewsd - Lobsters (Blog)')
        fg.link(href='http://localhost:5555', rel='alternate')  # TODO parameterize
        # fg.logo('http://ex.com/logo.jpg')
        fg.subtitle('Hackernewsd - Lobsters' if use_hackernews_url else 'Hackernewsd - Lobsters (Blog)')
        fg.language('en')
        for story in stories:
            fe = fg.add_entry()
            fe.title(story.title)
            fe.published(story.posted_date)
            fe.link(href=story.hacker_news_url if use_hackernews_url else story.url)

        rss = fg.rss_str(pretty=True).decode('utf-8')
        rss_file_path = Path.home() / ".hackernewsdrss_lobsters" if use_hackernews_url else Path.home() / ".hackernewsdrss_lobsters_blog"
        with open(rss_file_path, "w", encoding="utf-8") as rss_path:
            rss_path.write(rss)

    def cleanup_old_stories(self):
        Story.delete().where(Story.last_seen < datetime.now(timezone.utc) - timedelta(days=7)).execute()

    def get_old_stories(self):
        try:
            all_stories = list(Story.select().where(Story.type == StoryType.Lobsters.value))
            print(all_stories)
            return seq(all_stories).map(lambda s: self.entity_to_dto(s)).to_list()
        except Exception as e:
            return []

    def entity_to_dto(self, entity: Story) -> StoryDto:
        return StoryDto(entity.title, entity.url, entity.hnurl, datetime.fromisoformat(entity.last_seen).astimezone(timezone.utc), datetime.fromisoformat(entity.posted_date).astimezone(timezone.utc))

    def dto_to_entity(self, dto: StoryDto) -> Story:
        return Story(title=dto.title, url=dto.url, hnurl=dto.hacker_news_url, last_seen=dto.last_seen, posted_date=dto.posted_date, type=StoryType.Lobsters.value)

    def insert_new_stories(self, stories):
        for s in stories:
            entity = self.dto_to_entity(s)
            entity.save()

    def update_last_seen_dates(self, current_stories: list[StoryDto]):
        for story in current_stories:
            Story.update(last_seen=datetime.now(timezone.utc)).where((Story.type == StoryType.Lobsters.value) & (Story.hnurl == story.hacker_news_url) & (Story.posted_date == story.posted_date)).execute()

    def scrape(self):
        self.logger = self.get_logger()

        try:
            stopwatch = Stopwatch()
            self.cleanup_old_stories()
            old_stories = self.get_old_stories()
            rc_file = self.read_rc_file()
            queries = json.loads(rc_file)["queries"]
            all_current_stories = seq.range(1, 30).flat_map(lambda p: self.process_page(p)).to_list()
            self.update_last_seen_dates(all_current_stories)
            filtered_stories = seq(all_current_stories).filter(lambda x: seq(queries).map(lambda q: x.title.lower().find(q.lower()) != -1).any()).to_list()
            diff_stories = seq(filtered_stories).filter(lambda x: not seq(old_stories).filter(lambda y: y == x).any()).to_list()
            self.insert_new_stories(diff_stories)

            self.generate_rss(self.get_old_stories())
            self.generate_rss(self.get_old_stories(), True)

            stopwatch.stop()
            self.logger.info(f"It took {str(stopwatch)} for a full cycle for Lobsters.")
        except Exception as e:
            self.logger.error(f"Unhandled exception occurred", exc_info=True)
            print(e)
