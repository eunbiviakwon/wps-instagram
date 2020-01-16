import os

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.now()
        # instagram/.media/now.txt
        # 파일이 이미 있다면 다음줄에 기록
        # 파일이 없다면 파일을 생성하고 기록

        # os.path.abspath(__file__)
        # 추천: django.conf.settings의 내용을 쓰기
        with open(os.path.join(settings.MEDIA_ROOT, 'now.txt'), 'at') as f:
            time_str = f'Now: {timezone.localtime(now).strftime("%Y-%m-%d %H:%M:%S")}\n'
            f.write(time_str)
