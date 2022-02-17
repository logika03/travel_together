from functools import wraps

from django.db import transaction
from django.db.models import F

from blog.models import Article


def counted(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            counter = Article.objects.get(id=kwargs['pk'])
            counter.count_of_views += 1
            counter.save()
        return f(request, *args, **kwargs)

    return decorator
