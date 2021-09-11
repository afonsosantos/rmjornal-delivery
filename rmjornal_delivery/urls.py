from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('app/', include('delivery.urls')),
    path('', admin.site.urls),
]