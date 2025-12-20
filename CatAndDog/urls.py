"""
URL configuration for CatAndDog_ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from news import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'post', views.PostViewSet , basename='post')

# Настройка схемы API
schema_view = get_schema_view(
    openapi.Info(
        title="CatAndDog API",
        default_version='v1',
        description="Документация для вашего API",
        terms_of_service="Ссылка на условия использования",
        contact=openapi.Contact(email="Контактная информация(Email)"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Документация доступна всем
    permission_classes=(permissions.AllowAny,),  # Любой пользователь может просматривать
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("news.urls")),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
             schema_view.without_ui(cache_timeout=0),
             name='schema-json'),

    # Swagger UI (интерактивный интерфейс)
    re_path(r'^swagger/$',
             schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),

    # ReDoc (альтернативный интерфейс)
    re_path(r'^redoc/$',
             schema_view.with_ui('redoc', cache_timeout=0),
             name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL)

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Сайт питомника ""'
