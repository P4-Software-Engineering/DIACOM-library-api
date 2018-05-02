from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from library.permissions import IsDIACOM, IsDIACOMOrReadOnly, IsOwnerOrDIACOM
from .models import NominalBook as NominalBookModel, Book as BookModel, Location as LocationModel, \
    Donation as DonationModel, MyUser as MyUserModel
from .serializers import BookSerializer, UserSerializer, NominalBookSerializer, LocationSerializer, DonationSerializer


class NominalBook(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsDIACOMOrReadOnly]

    queryset = NominalBookModel.objects.all()
    serializer_class = NominalBookSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'author')


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
            nominal_book = NominalBookModel.objects.all()
            nominal_book = get_object_or_404(nominal_book, cod=book.cod_nominal_book)
            nominal_book.popularity = nominal_book.popularity + 1
            book.save()
            nominal_book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
