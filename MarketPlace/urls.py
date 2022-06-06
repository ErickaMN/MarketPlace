"""MarketPlace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from movies import views
from movies.views import GenreListView, MovieViewSet

router = DefaultRouter()
router.register('movies', MovieViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Blog project API",
      default_version='v1',
      description="This is test blog project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('v1/api/genres/', GenreListView.as_view()),
    path('v1/api/', include(router.urls)),
    path('v1/api/user/', include('user.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/movies/comments/', views.CommentListCreateView.as_view()),
    path('v1/api/movies/comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('v1/api/ratings/', include('ratings.urls')),
    path('v1/api/favorites/', views.UserFavoriteList.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
