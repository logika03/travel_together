"""searchpeople URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from blog.views import ArticlesPageListView, ArticlePageDetailView, last_articles_view, update_articles_view

app_name = 'blog'
urlpatterns = [
    path('', ArticlesPageListView.as_view(), name='articles'),
    re_path(r'^(?:article-(?P<pk>\d+)/)?$', ArticlePageDetailView.as_view(), name='article'),
    path('last-articles/', last_articles_view, name='last_articles'),
    path('update-articles/', update_articles_view, name='last_articles'),
]
