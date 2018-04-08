from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, UserManager
from django.db import models

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.title
    pass

class Location(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    #user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book + " - " + self.user + " - " + self.date
    pass


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