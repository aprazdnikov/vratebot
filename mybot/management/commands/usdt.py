from django.core.management.base import BaseCommand

from mybot.get_data import get_usdt


class Command(BaseCommand):
    help = 'Start my bot'

    def handle(self, *args, **options):
        if options['parse']:
            get_usdt()

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--parse',
            default=False,
            action='store_true',
            help='Запускает цикл получения курса USDT'
        )
