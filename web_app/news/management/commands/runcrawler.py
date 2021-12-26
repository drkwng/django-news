from django.core.management.base import BaseCommand
from news.crawlers.coindesk_crawler import run


class Command(BaseCommand):
    help = 'Run Crypto news crawling'

    def handle(self, *args, **options):
        run()
