import asyncio
import traceback
from selectolax.parser import HTMLParser
from httpx import AsyncClient
from src.parsers.news_item import NewsItem

class KommersantParser:
    DOCS_URL = 'https://www.kommersant.ru/doc/'
    NEWS_ROOT_URL = "https://www.kommersant.ru/lenta?from=all_lenta"
    AJAX_REQUEST_URL = "https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=3&listid=77&date=&intervaltype=&idafter="
    
    async def get_entities(self, count = 5):
        async with AsyncClient() as http_client:
            self.http_client = http_client
            try:
                links = await self._get_links(count)
                parsing_coroutines = [self._parse_article(l) for l in links]
                results = await asyncio.gather(*parsing_coroutines)
                return results
            except Exception:
                traceback.print_exc()
                return []
            
    async def _parse_article(self, url):
        response = await self.http_client.get(url)
        tree = HTMLParser(response.text)
        article_node = tree.css_first(f'article[data-article-url="{url}"]')
        title = article_node.css_first('h1').text().replace('\n', '').strip()
        paragraph_nodes = article_node.css('.doc__text')
        text = ' '.join([p.text() for p in paragraph_nodes])
        return NewsItem(url, title, text)
            
    async def _get_links(self, count):
        links = await self._get_root_page_links()
        last_link_id = links[-1].split('/')[-1]
        while len(links) < count:
            links.extend(await self._get_ajax_links_after(last_link_id))
            last_link_id = links[-1].split('/')[-1]
        return links[:count]

    async def _get_root_page_links(self):
        root_page = await self.http_client.get(KommersantParser.NEWS_ROOT_URL)
        tree = HTMLParser(root_page.text)
        articles = tree.css('article[data-article-url]')
        return [a.attributes['data-article-url'] for a in articles]
    
    async def _get_ajax_links_after(self, id):
        response = await self.http_client.get(self._construct_ajax_req_url(id))
        json_data = response.json()
        items = json_data['Items']
        return [self._construct_doc_url_for(i['DocsID']) for i in items]
        
    def _construct_ajax_req_url(self, id):
        return f'{KommersantParser.AJAX_REQUEST_URL}{id}'
    
    def _construct_doc_url_for(self, id):
        return f'{KommersantParser.DOCS_URL}{id}'
