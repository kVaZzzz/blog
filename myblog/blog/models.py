from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.EmailField(verbose_name='Почта', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='photo', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Post(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название поста', blank=False)
    content = models.TextField(verbose_name='Контент', blank=False, null=False)
    photo = models.ImageField(verbose_name='Фото к посту', upload_to='photo', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=254, verbose_name='Комментарий', blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Название поста', null=False)
    photo = models.ImageField(verbose_name='Фото комментария', upload_to='photo', null=True, blank=True)

    def __str__(self):
        return self.content


class UserPosted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class CommentCommented(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=254, verbose_name='Комментарий', blank=False)
    photo = models.ImageField(verbose_name='Фото комментария', upload_to='photo', null=True, blank=True)

    def __str__(self):
        return self.content
