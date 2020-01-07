from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    사용자모델로 쓰입니다
    """
    img_profile = models.ImageField('프로필이미지', blank=True, upload_to='userssadf/')