from vk_api import VkApi
import os

TOKEN = os.environ.get('VK_API_PUBLIC_TOKEN')
DOMAINS = ["tmrkt", ]
COUNT = 3


vk_session = VkApi(token=TOKEN)
API = vk_session.get_api()


def parse_public_by_query(query):
    urls = []

    for DOMAIN in DOMAINS:
        response = API.wall.search(
            domain=DOMAIN,
            query=query,
            count=COUNT
        )
        for item in response['items']:
            urls.append('https://vk.com/wall' + str(item['owner_id']) + '_' + str(item['id']))

    return urls
