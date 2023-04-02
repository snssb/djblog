from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.backends import ModelBackend

from .forms import (CommentForm, CreatePostForm, EditProfileForm,
                    PasswordChangingForm, ProfilePageForm, UserLoginForm,
                    UserRegisterForm)
from .models import Category, Comment, Post, Profile, Tag
from .templatetags.slugt import dj_slug


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')


class UpdatePostView(UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/update_post.html'


class CreatePost(CreateView):
    form_class = CreatePostForm
    template_name = 'blog/add_post.html'
    raise_exception = True

    # success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('post', kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        form.instance.slug = dj_slug(form.instance.title)
        form.instance.author_l = self.request.user
        form.instance.author = self.request.user.username
        form.save()
        return super().form_valid(form)


def LikeView(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post', args=[post.slug]) + '#anchor')
    return redirect('login')


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        print(self.request.user)
        sl = self.kwargs['slug']
        form.instance.post_id = Post.objects.get(slug=sl).id
        form.instance.name = self.request.user.username
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})


class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "blog/create_user_profile_page.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'blog/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'vkontakte_url', 'twitter_url', 'instagram_url', 'pinterest_url',
              'user_gender']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'blog/user_profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {"form": form})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')
    template_name = 'blog/change-password.html'


@login_required
def password_success(request):
    return render(request, 'blog/password_success.html', {})


class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'blog/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['item_selected'] = 'm'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author_l')


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = c
        context['item_selected'] = c.pk
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        likes = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = likes.total_likes()
        context = super().get_context_data(**kwargs)
        context["total_likes"] = total_likes
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db(fields=('views',))
        return context

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug']).prefetch_related('tags')


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('s')
        if query:
            queryset = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).filter(
                is_published=True)
        else:
            queryset = Post.objects.none()
        return queryset

    # return Post.objects.filter(title__icontains=self.request.GET.get('s')).filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get('s')
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={query}&"
        context['search_query'] = query
        return context
