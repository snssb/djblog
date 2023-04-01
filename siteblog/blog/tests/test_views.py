from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Post, Tag


class HomeListViewAndPaginateTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # User.objects.create_user('username', 'Pas$w0rd')
        Category.objects.create(title='Eda', slug='eda')
        Tag.objects.create(title='torty', slug='torty')

        number_of_posts = 8
        for post_num in range(number_of_posts):
            Post.objects.create(title='post %s' % post_num, slug='p0st %s' % post_num,
                                category_id=1)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertTemplateUsed(resp, 'blog/index.html')

    def test_pagination_is_six(self):
        resp = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(len(resp.context['object_list']) == 6)

    def test_list_next_page(self):
        resp = self.client.get(reverse('home')+'?page=2')
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['object_list']) == 2)
