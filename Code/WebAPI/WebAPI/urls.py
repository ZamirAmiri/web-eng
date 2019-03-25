
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('airports/', include('airports.urls')),
    path('carriers/', include('carriers.urls')),
]
