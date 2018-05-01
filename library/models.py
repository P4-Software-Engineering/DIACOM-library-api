from django.utils import timezone
from django.conf import settings

# from django.contrib.auth.models import User, UserManager
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class NominalBook(models.Model):
    cod = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    edition = models.IntegerField()
    volume = models.IntegerField()
    description = models.TextField()
    cover = models.TextField()


class Book(models.Model):
    cod_nominal_book = models.ForeignKey(NominalBook, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.cod_nominal_book.title


class Location(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_i = models.DateTimeField(default=timezone.now)
    date_f = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id_book + " - " + self.id_user + " - " + self.date_i + " - " + self.date_f


class Donation(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    book_title = models.CharField(max_length=300)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.book_title


'''
    Add attributes user
'''


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, first_name, **extra_fields):
        """
                Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, **extra_fields)

    def create_superuser(self, email, password, first_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, first_name, **extra_fields)


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # profile_pic = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    profile_pic = models.TextField(_('profile picture'), null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=300, null=True, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_DIACOM = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser
