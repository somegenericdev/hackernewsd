#TODO parameterize port (int)
#TODO parameterize notify (bool)
import os
import sys
from pathlib import Path

from flask import Flask, render_template_string, Response
from flask_apscheduler import APScheduler

from hackernewsd import HackerNewsScraper
from waitress import serve
import logging
from logging import handlers
from logging.handlers import RotatingFileHandler

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

def initLogger():
    logFilePath = str(Path.home() / ".hackernewsdlog")

    if not os.path.exists(logFilePath):
        with open(logFilePath, "w") as logFile:
            logFile.write("")

    log_formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")



    fileHandler = RotatingFileHandler(logFilePath, mode='a', maxBytes=25 * 1024 * 1024,
                                      backupCount=1, encoding=None, delay=0)
    fileHandler.setFormatter(log_formatter)
    fileHandler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(log_formatter)
    consoleHandler.setLevel(logging.INFO)

    rootLogger = logging.getLogger('root')
    rootLogger.setLevel(logging.INFO)

    rootLogger.addHandler(fileHandler)
    rootLogger.addHandler(consoleHandler)

if __name__ == '__main__':
    initLogger()
    scheduler.init_app(app)
    scheduler.start()
    serve(app, host="127.0.0.1", port=5555)
    #app.run(port=5555)