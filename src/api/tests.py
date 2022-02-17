from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.test import APITestCase

from blog.models import Article
from main.tests import signup_user


class ApiTests(APITestCase):

    def test_main_data(self):
        url = reverse('api:main')
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, {'status': 'ok'})

    def test_get_articles_not_auth_user(self):
        response = self.client.get('/api/articles/', format='json')
        self.assertEqual(response.status_code, 302)

    def test_get_post_articles(self):
        signup_user(self.client)
        url = reverse('api:article-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        add_article(self.client, 'Test', 'Test')
        add_article(self.client, 'Test2', 'Test2')
        self.assertEqual(Article.objects.count(), 2)

    def test_put_article(self):
        signup_user(self.client)
        cur_title = 'Test'
        cur_text = 'Test'
        new_title = 'New Test'
        add_article(self.client, cur_title, cur_text)
        article_id = Article.objects.first().id
        url = reverse('api:article-detail', args=[article_id])
        self.client.put(url, {'title': new_title, 'text': cur_text})
        article = get_object_or_404(Article, id=article_id)
        self.assertEqual(article.title, new_title)

    def test_delete_article(self):
        signup_user(self.client)
        cur_title = 'Test'
        cur_text = 'Test'
        add_article(self.client, cur_title, cur_text)
        cur_article_count = Article.objects.count()
        article_id = Article.objects.first().id
        url = reverse('api:article-detail', args=[article_id])
        self.client.delete(url)
        new_article_count = Article.objects.count()
        self.assertIsNot(cur_article_count, new_article_count)


def add_article(client, title, text):
    url = reverse('api:article-list')
    client.post(url, {
        'title': title,
        'text': text
    }, format='json')
