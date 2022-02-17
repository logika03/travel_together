from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Article

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id', 'title', 'text', 'count_of_views'
        )
        read_only_fields = ('count_of_views',)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(ArticleSerializer, self).create(validated_data)


class ArticleFullSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Article
        fields = (*ArticleSerializer.Meta.fields, 'author')
        read_only_fields = ('author',)
