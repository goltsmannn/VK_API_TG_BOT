from vk_api import VkApi
import os
import config

PUBLIC_TOKEN = config.VK_PUBLIC_TOKEN
DOMAINS = ["tmrkt", "brahand", "soldoutyeah", "stockmsk", "legitfammarket" ]
COUNT = 3
US_TO_EU = {
    '7': '40',
    '7.5': '40.5',
    '8': '41',
    '8.5': '42',
    '9': '42.5',
    '9.5': '43',
    '10': '44',
    '10.5': '44.5',
    '11': '45',
    '11.5': '45.5',
    '12': '46',
}

vk_session = VkApi(token=PUBLIC_TOKEN)
API = vk_session.get_api()


async def parse_public_by_query(query, type, size):
    urls = []
    sizes = []

    if size != 'Любой':
        sizes += size
        if type == 'Кроссовки':
            sizes += US_TO_EU.get(size)
            sizes += size.replace('.', ',')
            sizes += US_TO_EU.get(size).replace('.', ',')

    for DOMAIN in DOMAINS:
        flag = False
        urls.append('\n Поиск по %s: \n' % DOMAIN)
        if len(sizes):
            for size in sizes:
                response = API.wall.search(
                    domain=DOMAIN,
                    query=query + ' ' + size,
                    count=COUNT
                )
                for item in response['items']:
                    flag = True
                    urls.append('https://vk.com/wall' + str(item['owner_id']) + '_' + str(item['id']))
        else:
            response = API.wall.search(
                domain=DOMAIN,
                query=query,
                count=COUNT
            )
            for item in response['items']:
                flag = True
                urls.append('https://vk.com/wall' + str(item['owner_id']) + '_' + str(item['id']))
        if not flag:
            urls.append('По вашему запросу ничего не найдено')

    return urls
