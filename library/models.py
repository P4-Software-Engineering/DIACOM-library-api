from django.utils import timezone
from django.conf import settings

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, UserManager
from django.db import models


class NominalBook(models.Model):
    cod = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    edition = models.IntegerField()
    volume = models.IntegerField()
    description = models.TextField()


class Book(models.Model):
    cod_NominalBook = models.ForeignKey(NominalBook, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.cod_NominalBook.title


class Location(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_i = models.DateTimeField(default=timezone.now)
    date_f = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id_book + " - " + self.id_user + " - " + self.date_i + " - " + self.date_f


class Donation(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    book_title = models.CharField(max_length=300)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.book_title


'''
    Add attributes user
'''

class MyUserManager(BaseUserManager):
    def create_user(self, email, registry, password, name):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            registry=registry,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, registry, password, name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            registry=registry,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    registry = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    tee = models.FloatField(default=0)
    photo = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['registry', 'name']

    def __str__(self):
        return self.email

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
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin