from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles import views as profiles_views
from authentication import views as authentication_views


router = DefaultRouter()

router.register(r'users', profiles_views.UserViewSet)
router.register(r'user-roles', profiles_views.UserRoleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^login/?', authentication_views.LoginView.as_view()),
    url(r'^logout/?', authentication_views.LogoutView.as_view()),
    url(r'^me/?$', authentication_views.MeView.as_view()),

    url(r'^', include(router.urls)),
]
