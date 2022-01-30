# import sys
import logging
import re
from datetime import datetime

from slugify import slugify
from requests_html import HTMLSession
from django.utils.timezone import make_aware
from django.core.exceptions import ObjectDoesNotExist

from cache_memoize import cache_memoize

from celery import shared_task

from news.models import Article, Category, Author

# from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger('celery')


@cache_memoize(3600)
def get_author(u_id=3):
    return Author.objects.get(user_id=u_id)


def format_datetime(date):
    # datetime sample: 'Dec 6, 2021 at 7:11 p.m. UTC'
    replaced_daytime = re.sub('(a|p).m.', r'\1m', date)

    return make_aware(datetime.strptime(replaced_daytime, f'%b %d, %Y at %I:%M %p %Z'))


def scrape_data(response):
    data = {
        'name': response.html.xpath('//div[@class="at-headline"]/h1')[0].text.strip(),
        'short_description': response.html.xpath('//div[@class="at-subheadline"]/h2')[0].text.strip(),
        'content': response.html.xpath("//div[@class='at-text']/div"),
        'img_url': response.html.xpath('//div[@class="media"]/figure/img/@src')[0],
        'pub_date': response.html.xpath('//div[contains(@class, "at-created")]/div/span[contains(@class, "dHSCiD")]')[0].text,
        'pub_category': response.html.xpath('//div[@class="at-category"]/a/span')[0].text.strip()
    }
    return data


@shared_task
def crawl_one(url):
    author = get_author()
    try:

        with HTMLSession() as session:
            response = session.get(url)
            logger.info(response.content)

        logger.info(f'Parsing: {url}')

        data = scrape_data(response)

        my_content = ''
        for element in data['content']:
            my_content += f'<p>{element.text}</p>'

        img_name = slugify(data['name'])
        img_type = data['img_url'].split('.')[-1]

        img_path = f'images/{img_name}.{img_type}'

        with open(f'media/{img_path}', 'wb') as f:
            with HTMLSession() as session:
                response = session.get(data['img_url'])
                f.write(response.content)

        category = {
            'name': data['pub_category'],
            'slug': slugify(data['pub_category'])
        }

        article = {
            'name': data['name'],
            'slug': slugify(data['name']),
            'short_description': data['short_description'],
            'content': my_content,
            'main_image': img_path,
            'pub_date': format_datetime(data['pub_date']),
            'author': author,
        }
        # article, created = Article.objects.get_or_create(**article)
        try:
            article = Article.objects.get(slug=article['slug'])
        except ObjectDoesNotExist:
            article = Article.objects.create(**article)

        # cat, created = Category.objects.get_or_create(**category)
        try:
            cat = Category.objects.get(slug=category['slug'])
        except ObjectDoesNotExist:
            cat = Category.objects.create(**category)

        article.categories.add(cat)

    except Exception as e:
        logging.exception(e)
        # print(f'{url}', e, type(e), sys.exc_info()[-1].tb_lineno)

    logger.info(f'Success: {url}')


def get_fresh_urls():
    xml_url = 'https://www.coindesk.com/arc/outboundfeeds/news-sitemap-index/?outputType=xml'

    with HTMLSession() as session:
        r = session.get(xml_url)
        urls = re.findall(r'<loc>(https?://[^\s"]+)</loc>', r.content.decode())

    return urls[:30]


def run(task=None):
    # Article.objects.all().delete()

    fresh_news = get_fresh_urls()
    for url in fresh_news:
        crawl_one.delay(url)
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(crawl_one, fresh_news)

    if task:
        task.status = 'Succeed'
        task.done = True
        task.save()


if __name__ == '__main__':
    run()
