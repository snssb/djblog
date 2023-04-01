from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from blog.models import Post
from blog_api.permissions import IsOwnerOrReadOnly
from blog_api.serializers import (PostSerializerDetail, PostSerializerList,
                                  PostSerializerPhoto)


class PostListsPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000
    ordering = '-views'


class PostListView(generics.ListAPIView):
    """Получить список постов  /api/v1/posts/"""

    queryset = Post.objects.all()
    serializer_class = PostSerializerList
    pagination_class = PostListsPagination
    # lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    """Обновить пост, за исключением фото  /api/v1/posts/1"""

    serializer_class = PostSerializerDetail
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Post.objects.filter(pk=pk)




class PostPhotoView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    """Обновить фото поста  /api/v1/posts/photo/1/"""

    serializer_class = PostSerializerPhoto
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Post.objects.filter(pk=pk)

    def perform_create(self, serializer):
        serializer.save(author_l=self.request.user, datafile=self.request.data.get('photo'))
