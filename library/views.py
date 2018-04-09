from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NominalBook as NominalBookModel, Book as BookModel, Location as LocationModel, Donation as DonationModel, MyUser
from .serializers import BookSerializer, UserSerializer, NominalBookSerializer, LocationSerializer, DonationSerializer


class NominalBook(viewsets.ModelViewSet):
    queryset = NominalBookModel.objects.all()
    serializer_class = NominalBookSerializer


class Book(viewsets.ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer


class Location(viewsets.ModelViewSet):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer


class Donation(viewsets.ModelViewSet):
    queryset = DonationModel.objects.all()
    serializer_class = DonationSerializer


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data)
