from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from movies.models import Genre

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, profile_image, kakao_id, nickname, followings, like_genres, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            profile_image = profile_image,
            kakao_id = kakao_id,
            nickname = nickname,
            followings = followings,
            like_genres = like_genres,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, profile_image, kakao_id, nickname, followings, like_genres, password):
        user = self.create_user(
            email,
            password=password,
            profile_image = profile_image,
            kakao_id = kakao_id,
            nickname = nickname,
            followings = followings,
            like_genres = like_genres
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    profile_image = models.ImageField(default='accounts/avatar.png',)
    kakao_id = models.TextField(null=True)
    nickname = models.TextField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    like_genres = models.ManyToManyField(Genre, symmetrical=False, related_name='like_users')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile_image', 'nickname', 'followings','like_genres']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin