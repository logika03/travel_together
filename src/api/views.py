from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import api_view

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from api.serializers import ArticleFullSerializer, ArticleSerializer
from blog.models import Article
from api.tasks import send_mail_api


@api_view(['GET'])
def main_api_view(request):
    return Response({'status': 'ok'})


class ArticleChangeOnlyForOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id


@method_decorator(login_required, name='dispatch')
class ArticlesViewSet(viewsets.ModelViewSet):
    """Статьи"""
    pagination_class = LimitOffsetPagination
    pagination_classes = [ArticleChangeOnlyForOwnerPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleFullSerializer
        return ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Article.objects.select_related('author')
        if user.is_authenticated:
            qs = qs.filter(author=user)
        return qs


