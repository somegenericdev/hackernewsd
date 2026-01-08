import json
import os
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from flask import Flask, render_template_string, Response
from flask_apscheduler import APScheduler
from scrapers import HackerNewsScraper, LobstersScraper
from waitress import serve
import logging
from logging import handlers
from logging.handlers import RotatingFileHandler
from peewee import SqliteDatabase
from models import BaseModel, Story

app = Flask(__name__)
scheduler = APScheduler()


@app.route('/feed_hn_blog.xml')
def feedHnBlog():
    rssPath = Path.home() / ".hackernewsdrss_hn_blog"
    if os.path.exists(rssPath):
        with open(rssPath, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_hn.xml')
def feedHn():
    rssPath = Path.home() / ".hackernewsdrss_hn"
    if os.path.exists(rssPath):
        with open(rssPath, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_lobsters_blog.xml')
def feedLobstersBlog():
    rssPath = Path.home() / ".hackernewsdrss_lobsters_blog"
    if os.path.exists(rssPath):
        with open(rssPath, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_lobsters.xml')
def feedLobsters():
    rssPath = Path.home() / ".hackernewsdrss_lobsters"
    if os.path.exists(rssPath):
        with open(rssPath, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@scheduler.task('interval', id='scrapeJob', seconds=900, max_instances=1, next_run_time=datetime.now())
def scrapeJob():
    print('Executing scraping job.')
    hnScraper = HackerNewsScraper()
    hnScraper.scrape()
    lobstersScraper = LobstersScraper()
    lobstersScraper.scrape()


def readRcFile():
    rcFilePath = Path.home() / ".hackernewsdrc"
    with open(rcFilePath, "r", encoding="utf-8") as rcFile:
        return rcFile.read()


def initLogger():
    logFilePath = str(Path.home() / ".hackernewsdlog")

    if not os.path.exists(logFilePath):
        with open(logFilePath, "w", encoding="utf-8") as logFile:
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

def initDb():
    db = SqliteDatabase(Path.home() / "hnd.db")
    BaseModel._meta.database.initialize(db)
    db.connect()
    db.create_tables([Story])


if __name__ == '__main__':
    print(f"Starting Hackernewsd. Python version: {sys.version}")
    initLogger()
    initDb()
    rcFile = json.loads(readRcFile())
    scheduler.init_app(app)
    scheduler.start()
    serve(app, host=rcFile["host"], port=rcFile["port"])
    # app.run(port=5555)