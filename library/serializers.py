from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, serializers
from .models import Donation, Location, NominalBook, Book, MyUser as User


# Get the UserModel
UserModel = get_user_model()

class NominalBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = NominalBook
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'email', 'first_name', 'last_name', 'phone', 'profile_pic')
        read_only_fields = ('email', )
