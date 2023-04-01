from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from blog.models import Category, Post, Tag
from blog_api.serializers import PostSerializerList


class PostsApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('username', 'Pas$w0rd')
        Category.objects.create(title='Eda', slug='eda')
        Tag.objects.create(title='torty', slug='torty')

        number_of_posts = 8
        for post_num in range(number_of_posts):
            Post.objects.create(title='post %s' % post_num, slug='p0st %s' % post_num,
                                author_l=user, content='lorem test %s' % post_num, category_id=1)  # photo='test.png',

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')  # <TemplateResponse status_code=200, "text/html; charset=utf-8">
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('post-list'))
        # reg = reverse('post-list')  # /api/v1/posts/
        self.assertEqual(resp.status_code, 200)

    def test_get_data(self):
        resp = self.client.get(reverse('post-list'))
        posts = Post.objects.all()
        serializer_data = PostSerializerList(posts, many=True).data
        self.assertEqual(serializer_data[:6], resp.data.get('results'))

    def test_pagination_is_six(self):
        resp = self.client.get(reverse('post-list'))
        self.assertTrue('next' and 'previous' in resp.data)
        self.assertTrue(resp.data['results'])
        self.assertTrue(len(resp.data['results']) == 6)

    def test_list_next_page(self):
        resp = self.client.get(reverse('post-list') + '?page=2')
        self.assertTrue('next' and 'previous' in resp.data)
        self.assertTrue(resp.data['results'])
        self.assertTrue(len(resp.data['results']) == 2)
