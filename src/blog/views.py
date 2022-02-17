import json
from datetime import timedelta

from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from blog.decorators import counted
from blog.forms import CommentForm
from blog.models import Article, Comment
from blog.services import remove_like, add_like


class ArticlesPageListView(ListView):
    model = Article
    template_name = 'blog/main.html'
    context_object_name = 'article_list'


@method_decorator(counted, name='dispatch')
class ArticlePageDetailView(DetailView):
    template_name = 'blog/article.html'

    def get(self, request, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        return render(request, self.template_name, {
            'article': article,
            'user': user
        })

    def post(self, request, pk):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            author = self.request.user
            article = Article.objects.get(id=pk)
            text = form.cleaned_data['text']
            is_anonymous = form.cleaned_data['is_anonymous']
            comment = Comment(author=author, article=article, text=text, is_anonymous=is_anonymous)
            comment.save()
        return self.get(request, pk=pk)


class LikesView(DetailView):
    model = None

    def post(self, request, pk):
        article = Article.objects.get(id=pk)
        if article.like.get(like=request.user):
            remove_like(article, request.user)
            result = False
        else:
            add_like(article, request.user)
            result = True
        like_count = article.like.count()
        return HttpResponse(
            json.dumps({
                'result': result,
                'like_count': like_count,
            }),
            content_type='application/json'
        )


def last_articles_view(request):
    articles = Article.objects.filter(
        Q(title__startswith='Первая') | Q(title__startswith='Вторая'), author=request.user)
    return render(request, 'blog/partials/articles.html', {
        'articles': articles,
    })


def update_articles_view(request):
    articles = Article.objects.filter(updated_at__gt=F('created_at') + timedelta(days=3), author=request.user)
    return render(request, 'blog/partials/articles.html', {
        'articles': articles,
        'as': 'as'
    })
