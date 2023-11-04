import requests
import yaml
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from pathlib import Path
from loguru import logger
from requests.exceptions import RequestException
from src.tvwky.shared.project_config import GetConfig

# set up logging
logger.add("logs/runtime.log", rotation="500 MB", level="DEBUG")


class ScrapeSite:
    """
    The purpose of this class is to download .docx transcript files from https://www.thispodcastwillkillyou.com and save them to ~/data/raw/transcripts.

    Parameters
    ----------
    config_path : str
        The path to the configuration file.

    Returns
    -------
    None
        Files are saved to ~/data/raw/transcripts.
    
    Raises
    ------
    KeyError
        If the config file is missing required keys.

    Example
    -------
    >>> scraper = ScrapeSite("config/config.yaml")
    >>> scraper.scrape_site()
    """
    def __init__(self, config_path: str) -> None:
        config: Dict[str, Any] = GetConfig.get_config(config_path)
        logger.debug(f"Config contents: {config}")
        self.config: Dict[str, Any] = config["web_scraper"]
        
        required_keys: List[str] = ["url", "output_path"]
        missing_keys: List[str] = [key for key in required_keys if key not in self.config]

        if missing_keys:
            raise KeyError(f"Missing required keys in config: {', '.join(missing_keys)}")

        self.url: str = self.config.get("url")
        if not self.url:
            raise ValueError(f"'url' cannot be None.")
        
        self.output_path: str = self.config.get("output_path")
        if not self.output_path:
            raise ValueError(f"'output_path' cannot be None.")
    
    def scrape_site(self) -> None:
        """
        Function that scrapes a website for .docx files and saves them to ~/data/raw/transcripts.

        Parameters
        ----------
        None

        Returns
        -------
        None
            Files are saved to ~/data/raw/transcripts.
        
        Raises
        ------
        RequestException
            If the request to the website fails.

        Example
        -------
        >>> scraper = ScrapeSite("config/config.yaml")
        >>> scraper.scrape_site()
        """
        headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
        }
        delay: int = 1  # time delay in seconds

        try:
            response: requests.Response = requests.get(self.url, headers=headers)
        except RequestException as e:
            logger.error(f"Failed to download {self.url}. Exception: {e}.")
            raise

        if "Not Acceptable" in response.text:
            logger.error(f"Failed to download {self.url}. The server returned a 'Not Acceptable' response.")
            return

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        # Create output directory if it doesn't exist
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        
        for link in soup.find_all("a"):
            file_link: str = link.get("href", "")

            if file_link.endswith(".docx"):
                time.sleep(delay)  # delay between requests
                try:
                    response: requests.Response = requests.get(file_link, headers=headers)
                except RequestException as e:
                    logger.error(f"Failed to download {file_link}. Exception: {e}.")
                    raise

                filename: Path = Path(self.output_path) / file_link.split("/")[-1]

                with open(filename, "wb") as file:
                    file.write(response.content)
                logger.info(f"Downloaded {filename}")
