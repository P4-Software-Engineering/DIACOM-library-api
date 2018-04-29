from django.conf.urls import url, include
from django.contrib import admin
from library import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


router = DefaultRouter()
router.register(r'api/NominalBook', views.NominalBook)
router.register(r'api/Book', views.Book)
router.register(r'api/Location', views.Location)
router.register(r'api/Donation', views.Donation)
# router.register(r'api/UserList', views.UserList)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    # url(r'^user/$', views.CurrentUserView.as_view()),
    # url(r'^users/$', views.UserList.as_view()),
    url(r'^api/auth-jwt/', obtain_jwt_token),
    url(r'^api/auth-jwt-refresh/', refresh_jwt_token),
    url(r'^api/auth-jwt-verify/', verify_jwt_token),
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
]
