import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.tvwky.elt.spotify import GetSpotifyData

@patch("src.tvwky.shared.project_config.GetConfig.get_config")
def test_init_missing_keys(mock_get_config):
    mock_get_config.return_value = {}  # empty config
    with pytest.raises(KeyError):
        GetSpotifyData("some_path")

@patch("src.tvwky.shared.project_config.GetConfig.get_config")
def test_init_missing_show_uri(mock_get_config):
    mock_get_config.return_value = {"spotify":{"show_uri": None, "output_path": None}}  # keys with None
    with pytest.raises(ValueError):
        GetSpotifyData("some_path")

@patch("src.tvwky.shared.project_config.GetConfig.get_config")
@patch("src.tvwky.elt.spotify.Spotify")
def test_extract_data(mock_spotify, mock_get_config):
    # mocking configuration and Spotify API response
    mock_get_config.return_value = {"spotify":{"show_uri": "spotify:show:mock_uri", "output_path": "/Users/databug/grimoire/this-viz-will-kill-you/tests/test_output"}}
    mock_spotify_instance = MagicMock()
    mock_spotify.return_value = mock_spotify_instance
    mock_response = {
        "total": 1,
        "items": [
            {
                "id": "1",
                "name": "Episode1",
                "description": "Description1",
                "release_date": "2021-01-01",
                "duration_ms": 1000,
                "explicit": True,
            }
        ]
    }
    mock_spotify_instance.show_episodes.return_value = mock_response

    extractor = GetSpotifyData("some_path")
    df = extractor.extract_data()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["id"] == "1"
