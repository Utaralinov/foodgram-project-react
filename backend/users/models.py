import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


USERNAME_ME_ERROR = 'Username указан неверно! Нельзя указать username "me"'
INVALID_CHARACTER_ERR = ('Username указан неверно!'
                         'Можно использовать только латинские буквы,'
                         'цифры и @/./+/-/_')
REGEX = re.compile(r'^[\w.@+-]+\Z')


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            USERNAME_ME_ERROR
        )
    if not REGEX.match(value):
        raise ValidationError(
            INVALID_CHARACTER_ERR
        )
    return value


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя',
        validators=[username_validator]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [models.UniqueConstraint(fields=['username', 'email'],
                                               name='unique_username_email')]

    def __str__(self) -> str:
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_subscription')]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
