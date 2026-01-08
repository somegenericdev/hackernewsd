class StoryDto:
    def __init__(self, _title, _url, _hackerNewsUrl, _lastSeen, _postedDate):
        self.title = _title
        self.url = _url
        self.hackerNewsUrl = _hackerNewsUrl
        self.lastSeen = _lastSeen
        self.postedDate = _postedDate

    def __eq__(self, other):
        return self.url == other.url and self.postedDate == other.postedDate

class RateLimitException(Exception):
    pass