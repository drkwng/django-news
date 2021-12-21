import sys
import re
from datetime import datetime

from slugify import slugify
from requests_html import HTMLSession
from django.utils.timezone import make_aware

from concurrent.futures import ThreadPoolExecutor

from news.models import Article, Author, Category


# author, created = Author.objects.get_or_create(name='Coindesk')
AUTHOR = None


def format_datetime(date):
    # datetime sample: 'Dec 6, 2021 at 7:11 p.m. UTC'
    replaced_daytime = re.sub('(a|p).m.', r'\1m', date)

    return make_aware(datetime.strptime(replaced_daytime, f'%b %d, %Y at %I:%M %p %Z'))


def crawl_one(url):
    global AUTHOR

    if not AUTHOR:
        AUTHOR, created = Author.objects.get_or_create(name='Coindesk')

    try:

        with HTMLSession() as session:
            response = session.get(url)

        name = response.html.xpath('//div[@class="at-headline"]/h1')[0].text.strip()
        short_description = response.html.xpath('//div[@class="at-subheadline"]/h2')[0].text.strip()
        content = response.html.xpath("//div[@class='at-text']/div")
        img_url = response.html.xpath('//div[@class="media"]/figure/img/@src')[0]
        pub_date = response.html.xpath('//div[contains(@class, "at-created")]/div/span[contains(@class, "dHSCiD")]')[0].text
        pub_category = response.html.xpath('//div[@class="at-category"]/a/span')[0].text.strip()

        my_content = ''
        for element in content:
            my_content += f'<p>{element.text}</p>'

        img_name = slugify(name)
        img_type = img_url.split('.')[-1]

        img_path = f'images/{img_name}.{img_type}'

        with open(f'media/{img_path}', 'wb') as f:
            with HTMLSession() as session:
                response = session.get(img_url)
                f.write(response.content)

        category = {
            'name': pub_category,
            'slug': slugify(pub_category)
        }

        article = {
            'name': name,
            'slug': slugify(name),
            'short_description': short_description,
            'content': my_content,
            'main_image': img_path,
            'pub_date': format_datetime(pub_date),
            'author': author,
        }

        article, created = Article.objects.get_or_create(**article)

        cat, created = Category.objects.get_or_create(**category)
        article.categories.add(cat)

        print(article)

    except Exception as e:
        print(f'{url}', e, type(e), sys.exc_info()[-1].tb_lineno)


def get_urls():
    xml_url = 'https://www.coindesk.com/arc/outboundfeeds/news-sitemap-index/?outputType=xml'

    with HTMLSession() as session:
        r = session.get(xml_url)
        urls = re.findall(r'<loc>(https?://[^\s"]+)</loc>', r.content.decode())

    return urls


def run():
    # Article.objects.all().delete()
    urls = get_urls()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawl_one, urls)

