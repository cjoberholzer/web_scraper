import random

from scrapy import signals
import logging

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ErrorLoggingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls()
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def process_exception(self, request, exception, spider):
        logging.error(f"Error occurred processing request {request}: {exception}")
        return None  # Continue processing other middlewares

    def spider_opened(self, spider):
        logging.info(f'Spider opened: {spider.name}')

    def spider_closed(self, spider):
        logging.info(f'Spider closed: {spider.name}')


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
    Middleware to rotate the user agent for each request.
    """
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    # List of user agents can be found on the internet
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
        # Add more user agent strings here
    ]


class ProxyMiddleware(object):
    """
    Middleware to set a proxy for each request.
    """
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
