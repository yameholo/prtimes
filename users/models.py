import ulid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config.models import ULIDField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, screen_name, password, **extra_fields):
        """
        Create and save a user with the given email, email, and password.
        """
        if not email:
            raise ValueError('メールアドレスを設定してください。')
        if not screen_name:
            raise ValueError('ユーザー名を設定してください。')
        email = self.normalize_email(email)
        user = self.model(email=email, screen_name=screen_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, screen_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, screen_name, password, **extra_fields)

    def create_superuser(self, email, screen_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, screen_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(_("表示名"), max_length=64)
    screen_name = models.SlugField(_("ユーザ名"), max_length=15, unique=True)
    email = models.EmailField(_('メールアドレス'), unique=True)
    created_at = models.DateTimeField(_("登録日時"), default=timezone.now)

    is_staff = models.BooleanField(
        _('スタッフ'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('アクティブ'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['screen_name', ]

    class Meta:
        verbose_name = _('ユーザー')
        verbose_name_plural = _('ユーザー')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.screen_name
