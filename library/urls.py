from django.conf.urls import url, include
from django.contrib import admin
from library import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


router = DefaultRouter()
router.register(r'api/nominal_book', views.NominalBook)
router.register(r'api/book', views.Book)
# router.register(r'api/book_quantity', views.BookQuantity)
router.register(r'api/location', views.Location)
router.register(r'api/donation', views.Donation)
router.register(r'api/user', views.User)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),

    url(r'^api/book/list/(?P<cod_nominal_book>[0-9]+)/$', views.Book.as_view({'get': 'list'})),
    # url(r'^api/book_quantity/(?P<cod_nominal_book>[0-9]+)/$', views.BookQuantity.as_view({'get': 'retrieve'})),

    url(r'^api/auth-jwt/', obtain_jwt_token),
    url(r'^api/auth-jwt-refresh/', refresh_jwt_token),
    url(r'^api/auth-jwt-verify/', verify_jwt_token),
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
]
