import pytest
from loguru import logger
from src.tvwky.shared.project_config import GetConfig

# set up logging
logger.add("logs/tests.log", rotation="500 MB", level="DEBUG")

# Test if the constructor loads configuration properly
def test_load_config():
    config = GetConfig.get_config("tests/test_config/config_valid.yaml")
    assert config["web_scraper"]["url"] == "https://www.mockwebsite.com" # mocked url
    assert config["web_scraper"]["output_path"] == "/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output" # mocked path
    assert config["spotify"]["show_uri"] == "spotify:show:mock_uri"  # mocked uri
    assert config["spotify"]["output_path"] == "/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output" # mocked path