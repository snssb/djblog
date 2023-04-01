from django.urls import include, path

from . import views
# from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password/', PasswordsChangeView.as_view(), name='password'),
    path('password_success/', views.password_success, name="password_success"),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='blog/change-password.html')),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    path('post/add-post/', CreatePost.as_view(), name='add_post'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('post/<str:slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('post/edit/<str:slug>/', UpdatePostView.as_view(), name='update_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
]