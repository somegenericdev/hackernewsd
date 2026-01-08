class StoryDto:
    def __init__(self, _title, _url, _hacker_news_url, _last_seen, _posted_date):
        self.title = _title
        self.url = _url
        self.hacker_news_url = _hacker_news_url
        self.last_seen = _last_seen
        self.posted_date = _posted_date

    def __eq__(self, other):
        return self.url == other.url and self.posted_date == other.posted_date
    def __hash__(self):
        return hash((self.url, self.posted_date))

class RateLimitException(Exception):
    pass