from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import Article, Comment
from main.tests import signup_user

User = get_user_model()


class BlogTests(TestCase):
    def setUp(self):
        User.objects.create(
            first_name='Test',
            last_name='Test',
            birthday=datetime.now().date(),
            email='Test@test.ru',
            phone_number='8999999999',
            location='Kazan',
            password='Test'
        )
        user = User.objects.first()
        Article.objects.create(
            author=user,
            title='Test',
            text='Test'
        )
        Article.objects.create(
            author=user,
            title='Test2',
            text='Test2'
        )
        Article.objects.create(
            author=user,
            title='Test3',
            text='Test3'
        )
        self.user = user

    def test_article_title(self):
        article1 = Article.objects.get(text='Test')
        article2 = Article.objects.get(text='Test2')
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(str(article1), 'Test')
        self.assertEqual(article2.author.location, 'Kazan')

    def test_send_comment(self):
        c = Client()
        signup_user(c)
        article = Article.objects.first()
        url = reverse('blog:article', args=[article.id])
        c.post(url, {
            'text': 'Text',
            'is_anonymous': True,
        })
        comment = Comment.objects.filter(article=article).first()
        self.assertEqual(comment.text, 'Text')
