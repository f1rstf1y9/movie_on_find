from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

GENRE_CHOICES = [
    ('19',"모험"),
    ('18',"판타지"),
    ('17',"애니메이션"),
    ('16',"드라마"),
    ('15',"공포"),
    ('14',"액션"),
    ('13',"코미디"),
    ('12',"역사"),
    ('11',"서부"),
    ('10',"스릴러"),
    ('9',"범죄"),
    ('8',"다큐멘터리"),
    ('7',"SF"),
    ('6',"미스터리"),
    ('5',"음악"),
    ('4',"로맨스"),
    ('3',"가족"),
    ('2',"전쟁"),
    ('1',"TV영화"),
    (None, '선택')
]

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, profile_image, kakao_id, nickname, followings, password, like_genre):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            profile_image = profile_image,
            kakao_id = kakao_id,
            nickname = nickname,
            followings = followings,
            like_genre = like_genre,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, profile_image, kakao_id, nickname, followings, password, like_genre):
        user = self.create_user(
            email,
            password=password,
            profile_image = profile_image,
            kakao_id = kakao_id,
            nickname = nickname,
            followings = followings,
            like_genre = like_genre,
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
    profile_image = models.ImageField()
    kakao_id = models.TextField(null=True)
    nickname = models.TextField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    like_genre = models.TextField(choices=GENRE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile_image', 'nickname', 'followings',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin