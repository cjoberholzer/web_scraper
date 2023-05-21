from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd


class BaseScraper(ABC):
    """
    Base Scraper class that defines the standard structure for scrapers.
    It uses the Strategy Design Pattern.

    Design Pattern Implemented: Strategy
    """

    @abstractmethod
    def scrape_site(self, urls: List[str]) -> pd.DataFrame:
        """
        Method to scrape a site. This must be overridden by any base class.
        :param urls: A list of URLs to scrape.
        :return: a pandas DataFrame with the scraped data.
        """
        pass


class ScrapyScraper(BaseScraper):
    """
    Concrete Scraper that uses the Scrapy library for web scraping.
    """

    def scrape_site(self, urls: List[str]) -> pd.DataFrame:
        """
        Scrape the site using Scrapy.
        :param urls: A list of URLs to scrape.
        :return: a pandas DataFrame with the scraped data.
        """
        # We'll need to fill this in with the specifics of how to use Scrapy to scrape the data.
        pass


class WebScraper:
    """
    WebScraper uses a strategy to scrape web pages.
    """

    def __init__(self, scraper_strategy: BaseScraper):
        """
        Initialize the WebScraper with a specific scraping strategy.
        :param scraper_strategy: An instance of a class that implements BaseScraper.
        """
        self.scraper_strategy = scraper_strategy

    def scrape(self, urls: List[str]) -> pd.DataFrame:
        """
        Scrape the provided list of urls.
        :param urls: A list of URLs to scrape.
        :return: a pandas DataFrame with the scraped data.
        """
        return self.scraper_strategy.scrape_site(urls)
