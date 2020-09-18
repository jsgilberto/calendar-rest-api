from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
from .calendars.views import CalendarViewSet, EventViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'calendars', CalendarViewSet, basename='calendars')

calendars_router = routers.NestedSimpleRouter(router, r'calendars', lookup='calendar')
calendars_router.register(r'events', EventViewSet, basename='events')
# router.register(r'events', EventViewSet, basename='events')

schema_view = get_schema_view(
   openapi.Info(
      title="Calendar API",
      default_version='v1',
      description="A simple clone of the Google Calendar API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alv.mtz94@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(calendars_router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

    # path('', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
