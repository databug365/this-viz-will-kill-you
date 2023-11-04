import pytest
from unittest.mock import patch, mock_open, MagicMock, call
from loguru import logger
from pathlib import Path
from src.tvwky.elt.web_scraper import ScrapeSite
from requests.exceptions import RequestException

# set up logging
logger.add("logs/tests.log", rotation="500 MB", level="DEBUG")

# set up string for yaml file emulation
yaml_str = """web_scraper:
  url: 'https://www.mockwebsite.com'
  output_path: '/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output/'"""

# Test missing keys in configuration
def test_missing_keys():
    with pytest.raises(KeyError):
        ScrapeSite("tests/test_config/config_missing_keys.yaml")

# Test empty keys in configuration
def test_empty_keys():
    with pytest.raises(ValueError):
        ScrapeSite("tests/test_config/config_empty_keys.yaml")

# Test failed request to site
@patch('requests.get', side_effect=RequestException)
def test_request_exception(mock_get):
    scraper = ScrapeSite("tests/test_config/config_valid.yaml")
    with pytest.raises(RequestException):
        scraper.scrape_site()

# Test scrape_site function
@patch('src.tvwky.elt.web_scraper.requests.get')
@patch('builtins.open', new_callable=mock_open, read_data=yaml_str)
def test_scrape_site(mock_open_instance, mock_get):
    logger.debug("Starting test_scrape_site")

    # Create mock response for main page and files
    mock_response_main = MagicMock()
    mock_response_main.text = '<a href="file1.docx">File 1</a><a href="file2.docx">File 2</a>'
    
    mock_response_file = MagicMock()
    mock_response_file.content = b'some binary content'

    mock_get.side_effect = [mock_response_main, mock_response_file, mock_response_file]

    logger.debug("Mocked requests.get")

    scraper = ScrapeSite("tests/test_config/config_valid.yaml")
    logger.debug(f"Scraping {scraper.url}")
    logger.debug(f"Saving files to {scraper.output_path}")

    scraper.scrape_site()
    logger.debug(f"Finished scraping {scraper.url} with {mock_open_instance.call_args_list}")

    mock_open_instance.assert_has_calls([
        call(Path('/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output/file1.docx'), 'wb'),
        call(Path('/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output/file2.docx'), 'wb')
    ], any_order=True)
