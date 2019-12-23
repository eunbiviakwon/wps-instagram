from django.contrib import admin

from .models import Post, PostImage, PostComment, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass

# Register your models here.
