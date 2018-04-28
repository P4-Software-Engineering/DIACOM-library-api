from rest_framework import serializers, viewsets
from .models import Donation, Location, NominalBook, Book, MyUser as User


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