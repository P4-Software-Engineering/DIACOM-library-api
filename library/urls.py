from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


router = DefaultRouter()
router.register(r'api/NominalBook', views.NominalBook)
router.register(r'api/Book', views.Book)
router.register(r'api/Location', views.Location)
router.register(r'api/Donation', views.Donation)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^books/$', views.BookList.as_view()),
    url(r'^books/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),
    url(r'^user/$', views.CurrentUserView.as_view()),
    url(r'^users/$', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
