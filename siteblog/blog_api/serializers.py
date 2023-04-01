from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Category, Post


class PostSerializerList(serializers.ModelSerializer):
    author_l = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # lookup_field = 'slug'

    class Meta:
        model = Post
        fields = ('title', 'author_l', 'content', 'created_at', 'photo')


class PostSerializerDetail(serializers.ModelSerializer):
    author_l = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'author_l', 'content', 'category')


class PostSerializerPhoto(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('photo',)
