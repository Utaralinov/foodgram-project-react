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
        verbose_name='Пользователь',
        validators=[username_validator],
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self) -> str:
        return self.username