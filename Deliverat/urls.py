from django.contrib import admin
from django.urls import path, include

#rest APIs
from rest_framework import routers
from main import views as main_views
from items import views as item_views

#media imports
from django.conf import settings
from django.conf.urls.static import static

#rest APIs for routing in the app
router = routers.DefaultRouter()
#router.register(r'users', main_views.UserViewSet)
#router.register(r'groups', main_views.GroupViewSet)
#router.register(r'items', item_views.ItemViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('items.urls')),
    path('', include('request.urls')),
    #rest APIs
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
