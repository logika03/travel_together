from django.db import models

from main.models import BaseModel, User


class Article(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.TextField(verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    like = models.ManyToManyField(User, related_name='likes', verbose_name='Лайки', blank=True)
    count_of_views = models.IntegerField(default=0, verbose_name='Просмотры')

    readonly_fields = ['count_of_views']

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return self.title


class Image(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    path = models.CharField(max_length=100, verbose_name='Путь')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return self.path


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    text = models.TextField(verbose_name='Текст')
    is_anonymous = models.BooleanField()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text
