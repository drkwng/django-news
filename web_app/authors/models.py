from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile


class Author(UserenaBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='author_profile',
        on_delete=models.CASCADE
    )

    avatar = models.ImageField(upload_to='avatars')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user}'

