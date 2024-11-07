
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # stocks rotes
    path('', include('stocks.urls')),
    
]
