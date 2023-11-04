import yaml
from loguru import logger
import pandas as pd
from typing import List, Dict, Union, Any
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from src.tvwky.shared.project_config import GetConfig


class GetSpotifyData:
    config_path: str

    def __init__(self, config_path: str) -> None:
        config: Dict[str, Any] = GetConfig.get_config(config_path)
        logger.debug(f"Config contents: {config}")
        self.config: Dict[str, Any] = config["spotify"]
        
        required_keys: list = ["show_uri", "output_path"]
        missing_keys: list = [key for key in required_keys if key not in self.config]

        if missing_keys:
            raise KeyError(f"Missing required keys in config: {', '.join(missing_keys)}")
        
        self.show_uri: str = self.config.get("show_uri")
        if not self.show_uri:
            raise ValueError(f"'show_uri' cannot be None.")
    
    def extract_data(self) -> pd.DataFrame:
        """
        Function that extracts podcast data from spotify

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            The dataframe containing the podcast data.
        """
        spotify: Spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())

        data: List[Dict[str, Union[str, int, bool]]] = []

        total: int = 1 # temporary variable
        offset: int = 0

        while offset < total:
            results: Dict[str, Union[str, int, bool]] = spotify.show_episodes(self.show_uri, limit=50, offset=offset)
            total: int = results['total']
            offset += 50 # increases the offset

            for episode in results['items']:
                episode_data: Dict[str, Union[str, int, bool]] = {
                    'id': episode['id'],
                    'title': episode['name'],
                    'description': episode['description'],
                    'release_date': episode['release_date'],
                    'duration_ms': episode['duration_ms'],
                    'explicit': episode['explicit'],

                }
                data.append(episode_data)
        
        return pd.DataFrame(data)

    def load_data(self, df: pd.DataFrame) -> None:
        df.to_csv(self.config['output_path'])
