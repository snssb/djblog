from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserChangeForm, UserCreationForm)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Comment, Post, Profile


class ProfilePageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'vkontakte_url', 'twitter_url', 'instagram_url', 'pinterest_url', 'user_gender')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-label'}),
            'website_url': forms.TextInput(attrs={'class': 'form-label'}),
            'vkontakte_url': forms.TextInput(attrs={'class': 'form-label'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-label'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-label'}),
            'pinterest_url': forms.TextInput(attrs={'class': 'form-label'}),
        }

        labels = {
            'bio': 'Биография',
            'profile_pic': 'Аватарка',
            'website_url': 'Сайт',
            'vkontakte_url': 'ВК',
            'twitter_url': 'Твиттер',
            'instagram_url': 'Инста',
            'pinterest_url': 'Пинтерест',
            'user_gender': 'Пол',
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-label'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-label'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-label'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-label'}))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-label'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-label'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        mail = self.cleaned_data['email']
        chk = User.objects.filter(email=mail)
        if chk:
            raise ValidationError(('Данный email уже зарегистрирован'), code='error_mail')

        return mail


class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=120, label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=120, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=120, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=120, label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length=120, label='Последнее посещение', widget=forms.HiddenInput())
    date_joined = forms.CharField(max_length=120, label='Дата регистрации', widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=120, label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=120, label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=120, label='Повторите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-label3'}),
        }

        labels = {
            'body': 'Ваш комментарий:',
        }


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'photo', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-label'}),
            'content': forms.Textarea(attrs={'class': 'ck_content form-label'}),
            'category': forms.Select(attrs={'class': 'form-label'}),
        }
