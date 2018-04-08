from rest_framework import serializers, viewsets
from .models import Book, MyUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'version', 'code', 'image')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'registry', 'photo', 'tee', 'name')