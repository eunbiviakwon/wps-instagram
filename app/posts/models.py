import re

from django.db import models

from members.models import User


class Post(models.Model):
    TAG_PATTERN = re.compile(r'#(\w+)')
    """
    인스타그램의 포스트
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    like_users = models.ManyToManyField(
        User, through='PostLike', related_name='like_post_set',
    )
    tags = models.ManyToManyField(
        'Tag', verbose_name='해시태그 목록', related_name='posts', blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{author} | {created}'.format(
            author=self.author.username,
            created=self.created,
        )

    def _save_html(self):
        """
        content속성의 값을 사용해서 해시태그에 해당하는 문자열을 a태그로 바꾸어 줌
        :return: 해시태그가 a태그로 변환된 HTML
        """
        self.content_html = re.sub(
            self.TAG_PATTERN,
            r'<a href="/explore/tags/\g<1>/">#\g<1></a>',
            self.content,
        )

    def _save_tags(self):
        """
        content에 포함된 해시태그 문자열 (ex: #Python)의 Tag들을 만들고,
        자신의 tags Many-to-many field에 추가한다
        """
        tag_name_list = re.findall(self.TAG_PATTERN, self.content)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_name_list]
        self.tags.set(tags)

    def save(self, *args, **kwargs):
        self._save_html()
        super().save(*args, **kwargs)
        self._save_tags()


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    """
    사용자가 좋아요 누른 Post정보를 저장
    Many-to-many필드를 중간모델(Intermediate Model)을 거쳐 사용
     언제 생성되었는지를 Extra field로 저장! (created)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    """
    Many-to-many에서, 필드는 Post에 클래스에 작성
    HashTag의 Tag를 담당
    Post입장에서 post.tags.all()로 연결된 전체 Tag를 불러올 수 있어야 함
    Tag 입장에서 tag.posts.all()로 연결된 전체 Post를 불러올 수 있어야 함
    Django admin에서 결과를 볼 수 있도록 admin.py에 적절히 내용 기록
    중개모델(Intermediate model)을 사용할 필요 없음
    """
    name = models.CharField('태그명', max_length=100)

    def __str__(self):
        return self.name