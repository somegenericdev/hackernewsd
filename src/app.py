#TODO parameterize port (int)
#TODO parameterize notify (bool)
import os
from pathlib import Path

from flask import Flask, render_template_string, Response
from flask_apscheduler import APScheduler

from hackernewsd import HackerNewsScraper

app = Flask(__name__)
scheduler = APScheduler()


@app.route('/feed.xml')
def feed():
    rssPath = Path.home() / ".hackernewsdrss"
    if os.path.exists(rssPath):
        with open(rssPath, "r") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404

@app.route('/feed_hn.xml')
def feedHn():
    rssPath = Path.home() / ".hackernewsdrss_hn"
    if os.path.exists(rssPath):
        with open(rssPath, "r") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@scheduler.task('interval', id='scrapeJob', seconds=60, max_instances=1)
def scrapeJob():
    print('Executing scraping job.')
    scraper = HackerNewsScraper()
    scraper.scrape()


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=5555)
