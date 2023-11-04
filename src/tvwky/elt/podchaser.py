"""
Developer's note: The code below is incomplete. There are not enough consistent ratings to make extracting this data worthwhile.
Might revisit in the future. For now, no loading module has been written and the config module has not been implemented.
"""

from python_graphql_client import GraphqlClient
import os
from loguru import logger

# set up logging
logger.add("logs/runtime.log", rotation="500 MB", level="DEBUG")


class PodchaserData:
    def __init__(self):
        pass

    def __get_token(self) -> str:
        query = f"""
        mutation {{
            requestAccessToken(
                input: {{
                    grant_type: CLIENT_CREDENTIALS
                    client_id: "{os.getenv('PODCHASER_DEV_KEY')}"
                    client_secret: "{os.getenv('PODCHASER_DEV_SECRET')}"
                }}
            ) {{
                access_token
            }}
        }}
        """

        # Execute the GraphQL call using our API's endpoint and your query.
        response = GraphqlClient(endpoint="https://api.podchaser.com/graphql").execute(query=query)

        # Access the returned data.
        access_token = response['data']['requestAccessToken']['access_token']

        return access_token
    
    def get_podchaser_data(self):
        access_token = self.__get_token()

        podcast_id = "1299915173"
        podcast_identifier_type = "APPLE_PODCASTS"

        podchaser_endpoint = "https://api.podchaser.com/graphql"

        query = f"""
        query {{
            podcast(identifier: {{
                id: "{podcast_id}",
                type: {podcast_identifier_type}
            }}) {{
                episodes {{
                    data {{
                        title,
                        description,
                        airDate,
                        length,
                        explicit,
                        episodeType,
                        ratingAverage,
                        ratingCount,
                        reviewCount,
                        reviews {{
                            data {{
                                rating {{
                                    rating
                                }},
                                content
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """


        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = GraphqlClient(endpoint=f"{podchaser_endpoint}", headers=headers).execute(query=query)

        logger.info(response)

if __name__ == '__main__':
    podcast = PodchaserData()
    podcast.get_podchaser_data()