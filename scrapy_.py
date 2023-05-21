import logging
from typing import List

import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from scrapy.crawler import CrawlerProcess
from pipeline import DocItem
from scraper import BaseScraper


from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.spiders import Spider, Rule


class ScrapySpider(Spider):
    """
    Spider class to be used with ScrapyScraper.
    """
    name = 'doc_spider'
    allowed_domains = ['python.langchain.com']
    start_urls = []  # This will be filled dynamically

    custom_settings = {
        'ITEM_PIPELINES': {'pipeline.JsonExportPipeline': 1},  # Used for Pipeline order
        'LOG_LEVEL': 'INFO',
        'DOWNLOADER_MIDDLEWARES': {
            # '__main__.RotateUserAgentMiddleware': 110,
            # '__main__.ProxyMiddleware': 100
            'middleware.ErrorLoggingMiddleware': 543,
        },
    }

    def __init__(self, crawler, urls=None, *args, **kwargs):
        self.crawler = crawler
        super().__init__(*args, **kwargs)
        if urls is not None:
            self.start_urls = urls

        # Connect the spider_closed handler to the spider_closed signal
        self.crawler.signals.connect(self.spider_closed, signals.spider_closed)

        self.crawler.signals.connect(self.handle_spider_error, signals.spider_error)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(crawler, *args, **kwargs)

    def spider_closed(self, spider, reason):
        """
        This method is called when the spider finishes crawling.
        :param spider: The spider instance that was closed.
        :param reason: A string representing the reason why the spider was closed.
        """
        pass  # Add any cleanup or post-processing code here

    def parse(self, response):
        item = DocItem()
        item['api_docs'] = response.css('pre::text').getall()  # extracting API documentation
        item['explanatory_text'] = response.css('p::text').getall()  # extracting explanatory text
        yield item

    def handle_spider_error(self, failure, response, spider):
        """
        This method is called when an error is raised while processing a response.
        :param failure: A Twisted Failure instance that encapsulates the error.
        :param response: The Response object that was being processed when the error happened.
        :param spider: The Spider instance that raised the error.
        """
        # We log the error here and ignore the request
        self.logger.error(f"Error processing {response.url}: {failure}", exc_info=True)
        raise IgnoreRequest


class ScrapyScraper(BaseScraper, scrapy.Spider):
    """
    Concrete Scraper that uses the Scrapy library for web scraping.
    """
    name = 'test_spider'

    def scrape_site(self, urls: List[str]) -> pd.DataFrame:
        """
        Scrape the site using Scrapy.
        :param urls: A list of URLs to scrape.
        :return: a pandas DataFrame with the scraped data.
        """
        process = CrawlerProcess()
        process.crawl(ScrapySpider, urls=urls)
        process.start()  # the script will block here until the crawling is finished

        # Wrap the file reading code with try/except
        try:
            # TODO: Read the output JSON file into a pandas DataFrame
            df = pd.read_json("output/items.json")
            df.to_csv('output.csv', index=False)
            # return df
        except FileNotFoundError:
            self.logger.error('Failed to read JSON file. File not found.', exc_info=True)
        except Exception as e:
            self.logger.error('Failed to read JSON file. Unexpected error.', exc_info=True)


"""
Running the scraper
"""
LOG_LEVEL = 'DEBUG'
scrapy_scraper = ScrapyScraper()
scrapy_scraper.scrape_site(["https://python.langchain.com/en/latest/index.html"])
