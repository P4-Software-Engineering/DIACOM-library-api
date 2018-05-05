from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from library.permissions import IsDIACOM, IsDIACOMOrReadOnly, IsOwnerOrDIACOM
from .models import NominalBook as NominalBookModel, Book as BookModel, Location as LocationModel, \
    Donation as DonationModel, MyUser as MyUserModel
from .serializers import BookSerializer, UserSerializer, NominalBookSerializer, LocationSerializer, DonationSerializer
import datetime


class NominalBook(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsDIACOMOrReadOnly]

    queryset = NominalBookModel.objects.all()
    serializer_class = NominalBookSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'author')


class NominalBookTop10(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = NominalBookModel.objects.all().order_by('-popularity')[:10]
        serializer = NominalBookSerializer(queryset, many=True)
        return Response(serializer.data)


class Book(viewsets.GenericViewSet,
           mixins.CreateModelMixin,
           mixins.DestroyModelMixin,
           mixins.UpdateModelMixin,
           mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, IsDIACOM]

    queryset = BookModel.objects.all()
    serializer_class = BookSerializer

    def list(self, request, cod_nominal_book):
        queryset = BookModel.objects.filter(cod_nominal_book=cod_nominal_book).order_by('available')
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class BookQuantity(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsDIACOM]

    def retrieve(self, request, cod_nominal_book):
        queryset = BookModel.objects.filter(cod_nominal_book=cod_nominal_book)
        quantity = len(queryset)

        return Response(quantity)


class Location(viewsets.GenericViewSet,
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

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            book = BookModel.objects.all()
            book = get_object_or_404(book, cod=request.data.__getitem__('cod_book'))
            if book.available is False:
                return Response('Livro já alocado! Tente com outro livro!', status=status.HTTP_400_BAD_REQUEST)
            book.available = False
            book.cod_nominal_book.popularity += 1
            book.cod_nominal_book.save()
            serializer.save()
            book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationExpired(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsDIACOM]

    def list(self, request):
        queryset = LocationModel.objects.filter(closed=False, date_f__lt=datetime.date.today()).order_by('date_f')
        serializer = LocationSerializer(queryset, many=True)

        return Response(serializer.data)


class Donation(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsDIACOM]

        return [permission() for permission in permission_classes]

    queryset = DonationModel.objects.all()
    serializer_class = DonationSerializer


class User(viewsets.GenericViewSet,
           mixins.ListModelMixin,
           mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, IsDIACOM]

    queryset = MyUserModel.objects.all()
    serializer_class = UserSerializer

    filter_backends = (filters.SearchFilter, )
    search_fields = ('first_name', 'last_name', 'email')
