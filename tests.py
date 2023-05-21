import unittest
from unittest.mock import patch, Mock

from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse

from scrapy_ import ScrapySpider


class TestScrapySpider(unittest.TestCase):
    def setUp(self):
        # This method will be called before every test
        self.spider = ScrapySpider()

    def test_parse(self):
        # Here we're going to test the parse method by simulating a response
        # and checking if the parse method returns the correct data.

        # Let's assume we have a page with one <pre> tag and two <p> tags
        html_body = """
        <html>
            <body>
                <pre>API Documentation</pre>
                <p>Explanatory text 1</p>
                <p>Explanatory text 2</p>
            </body>
        </html>
        """
        url = 'http://python.langchain.com/en/latest/index.html'
        request = self.spider.make_requests_from_url(url)
        response = HtmlResponse(url=url, request=request, body=html_body, encoding='utf-8')

        # Call the spider's parse method
        result = next(self.spider.parse(response))

        # Check if the result is as expected
        expected_item = {
            'api_docs': ['API Documentation'],
            'explanatory_text': ['Explanatory text 1', 'Explanatory text 2']
        }
        self.assertEqual(result, expected_item)

    @patch.object(ScrapySpider, 'logger')
    def test_handle_spider_error(self, mock_logger):
        # Here we're going to test if errors are handled correctly
        # by the handle_spider_error method.
        # We're going to use the patch.object decorator to replace the logger
        # with a Mock object, so we can check if the error method was called correctly.

        failure = Mock()
        response = Mock()
        spider = Mock()

        # Let's simulate an error
        failure.getErrorMessage.return_value = 'An error occurred'

        # Call the handle_spider_error method
        with self.assertRaises(IgnoreRequest):
            self.spider.handle_spider_error(failure, response, spider)

        # Check if the logger's error method was called with the correct message
        mock_logger.error.assert_called_once_with('Error processing None: An error occurred')

if __name__ == '__main__':
    unittest.main()
