from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('app/', include('delivery.urls')),
    path('', admin.site.urls),
]
