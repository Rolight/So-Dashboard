from pprint import pprint

from django.core.management.base import BaseCommand
from django.utils import timezone

from so.models import Website
from so import core
from so.constant import constant


class Command(BaseCommand):
    help = """
        auto run spider
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            '--mode',
            action='store',
            dest='mode',
            help='Please specify mode'
        )

    def handle(self, *args, **options):
        smode = dict(constant.SCHEDULE_MODE)
        cur_mode = options.get('mode')
        if not cur_mode:
            print('need mode')
            return
        mode_code = smode[cur_mode]
        for website in Website.objects.filter(schedule_type=mode_code):
            print('processing website %s' % website.title)
            task = core.create_website_spider_task(website.pk)
            pprint(task)
            core.run_task(task)
        print('mode %s finished' % cur_mode)
