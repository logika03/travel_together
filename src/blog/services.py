from blog.models import Article


def add_like(article, user):
    article.like.add(user)


def remove_like(article, user):
    article.like.remove(user)


