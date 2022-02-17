from django.contrib import admin

from blog.models import Article, Image, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'get_count_of_likes', 'count_of_views', 'text')
    list_display_links = ('title',)
    list_filter = ('created_at', 'updated_at', 'author')
    ordering = ('-count_of_views',)

    def get_count_of_likes(self, obj):
        return obj.like.count()

    get_count_of_likes.short_description = 'likes'


class ImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'path')
    list_filter = ('article',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'text')
    list_display_links = ('article',)
    list_filter = ('author',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
