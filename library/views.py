from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from library.permissions import IsDIACOM, IsDIACOMOrReadOnly, IsOwnerOrDIACOM
from .models import NominalBook as NominalBookModel, Book as BookModel, Location as LocationModel, Donation as DonationModel, MyUser as MyUserModel
from .serializers import BookSerializer, UserSerializer, NominalBookSerializer, LocationSerializer, DonationSerializer


class NominalBook(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsDIACOMOrReadOnly]

    queryset = NominalBookModel.objects.all()
    serializer_class = NominalBookSerializer


class Book(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDIACOM]

    queryset = BookModel.objects.all()
    serializer_class = BookSerializer


class Location(viewsets.GenericViewSet,
               mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin):
    def get_permissions(self):
        if self.action in ('list', 'create', 'update'):
            permission_classes = [IsAuthenticated, IsDIACOM]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrDIACOM]

        return [permission() for permission in permission_classes]

    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer


class Donation(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsDIACOM]

        return [permission() for permission in permission_classes]

    queryset = DonationModel.objects.all()
    serializer_class = DonationSerializer


# class UserList(generics.ListCreateAPIView):
#     queryset = MyUserModel.objects.all()
#     serializer_class = UserSerializer

#
# class CurrentUserView(APIView):
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         print(serializer.data)
#         return Response(serializer.data)
