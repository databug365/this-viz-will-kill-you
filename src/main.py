import click
from pathlib import Path
from src.tvwky.elt.web_scraper import ScrapeSite
from src.tvwky.elt.spotify import GetSpotifyData

@click.command()
@click.option('--config', default='/Users/databug/grimoire/this-viz-will-kill-you/config/config.yaml', type=click.Path(exists=True), help="Path to the configuration YAML file.")
def main(config):
    """
    Scrape documents from a website.
    """

    # check if transcripts directory exists
    directory = Path("/Users/databug/grimoire/this-viz-will-kill-you/data/raw/transcripts")

    if directory.exists():
        pass
    else:
        # Initialize the scraper with the config file
        scraper = ScrapeSite(config)

        # Start the scraping process
        scraper.scrape_site()
    
    # instantiate the ExtractSpotify class
    spotify = GetSpotifyData(config)

    # extract the data
    podcast_df = spotify.extract_data()

    # load the data
    spotify.load_data(podcast_df)

if __name__ == '__main__':
    main()
