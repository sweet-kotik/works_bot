import asyncio
import httpx
import feedparser
import datetime
from aiogram.methods import send_message
from collections import deque
from aiogram.types import Message

# rss_link = 'https://156.ru/api/ads.php?f=get_ads&cat=rezume&rss'
# rss_link ='https://156.ru/api/ads.php?f=get_ads&cat=vacancy&rss'

n_test_chars = 50
posted_q = deque(maxlen=20)
httpx_client = httpx.AsyncClient()
home_site_link = 'https://156.ru'

async def work_parser(message: Message, CHAT_ID):
    

    rss_link = 'https://156.ru/api/ads.php?f=get_ads&cat=rezume&rss'

    while True:
        try:
            response = await httpx_client.get(rss_link)
        except:
            await asyncio.sleep(10)
            continue

        feed = feedparser.parse(response.text)

        for entry in feed.entries[5::-1]:
            title = entry.title
            link = entry.link
            published = datetime.datetime.strptime(entry.published, '%Y-%m-%d %H:%M:%S')

            news_text = f'<a href="{link}">{title}</a>\n\n<a href="{home_site_link}">156.ru</a> • {published:%b %d, %Y}'
            head = news_text[:n_test_chars].strip()

            if head in posted_q:
                continue
            
            await message.bot.send_message(
                CHAT_ID,
                news_text,
                parse_mode='HTML'
            )
            
            posted_q.appendleft(head)

        await asyncio.sleep(5)

    