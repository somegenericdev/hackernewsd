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
def feed_hn_blog():
    rss_path = Path.home() / ".hackernewsdrss_hn_blog"
    if os.path.exists(rss_path):
        with open(rss_path, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_hn.xml')
def feed_hn():
    rss_path = Path.home() / ".hackernewsdrss_hn"
    if os.path.exists(rss_path):
        with open(rss_path, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_lobsters_blog.xml')
def feed_lobsters_blog():
    rss_path = Path.home() / ".hackernewsdrss_lobsters_blog"
    if os.path.exists(rss_path):
        with open(rss_path, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/feed_lobsters.xml')
def feed_lobsters():
    rss_path = Path.home() / ".hackernewsdrss_lobsters"
    if os.path.exists(rss_path):
        with open(rss_path, "r", encoding="utf-8") as rss:
            return Response(rss.read(), mimetype='text/xml')
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@scheduler.task('interval', id='scrapeJob', seconds=900, max_instances=1, next_run_time=datetime.now())
def scrape_job():
    logger = get_logger()
    logger.info('Executing scraping job.')
    hn_scraper = HackerNewsScraper()
    hn_scraper.scrape()
    lobsters_scraper = LobstersScraper()
    lobsters_scraper.scrape()


def read_rc_file():
    rc_file_path = Path.home() / ".hackernewsdrc"
    with open(rc_file_path, "r", encoding="utf-8") as rc_file:
        return rc_file.read()


def init_logger():
    log_file_path = str(Path.home() / ".hackernewsdlog")

    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8") as logFile:
            logFile.write("")

    log_formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(log_file_path, mode='a', maxBytes=25 * 1024 * 1024,
                                       backupCount=1, encoding=None, delay=0)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(log_formatter)
    consoleHandler.setLevel(logging.INFO)

    rootLogger = logging.getLogger('root')
    rootLogger.setLevel(logging.INFO)

    rootLogger.addHandler(file_handler)
    rootLogger.addHandler(consoleHandler)


def init_db():
    db = SqliteDatabase(Path.home() / "hnd.db")
    BaseModel._meta.database.initialize(db)
    db.connect()
    db.create_tables([Story])


def get_logger():
    root_logger = logging.getLogger('root')
    return root_logger


if __name__ == '__main__':
    init_logger()
    init_db()
    logger = get_logger()
    logger.info(f"Starting Hackernewsd. Python version: {sys.version}")
    rc_file = json.loads(read_rc_file())
    scheduler.init_app(app)
    scheduler.start()
    serve(app, host=rc_file["host"], port=rc_file["port"])
    # app.run(port=5555)
