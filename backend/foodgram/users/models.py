from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        'Email', unique=True, max_length=254,
        help_text='Введите адрес электронной почты')
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        help_text='Будет показано на сайте')
    first_name = models.CharField(
        'Имя', max_length=150)
    last_name = models.CharField(
        'Фамилия', max_length=150)

    class Meta:
        ordering = ('id', )
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'