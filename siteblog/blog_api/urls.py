from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from blog_api.views import PostDetailView, PostListView, PostPhotoView

router = routers.SimpleRouter()
router.register(r'posts', PostDetailView, basename='post')
router.register(r'posts/photo', PostPhotoView, basename='post')



urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('', include(router.urls)),
    # path('drf-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('posts/<int:pk>', PostDetailView.as_view(), name='post-list')
]
