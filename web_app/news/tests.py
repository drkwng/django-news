from django.test import TestCase
from news.crawlers.coindesk_crawler import \
    get_fresh_urls, scrape_data

import traceback
from requests_html import HTMLSession


class CrawlerTestCase(TestCase):

    def test_xml_is_available(self):
        xml = 'https://www.coindesk.com/arc/outboundfeeds/news-sitemap-index/?outputType=xml'
        with HTMLSession() as session:
            r = session.get(xml)
        self.assertTrue(r.status_code == 200)

    def test_article_regex(self):
        urls = get_fresh_urls()[:5]
        data_list = []
        for url in urls:
            try:
                with HTMLSession() as session:
                    r = session.get(url)
                    data = scrape_data(r)
                    data_list.append(data)
            except IndexError:
                print(f'RegExp problem at {url} \n{traceback.format_exc()}')

        self.assertTrue(len(data_list) < 5)
