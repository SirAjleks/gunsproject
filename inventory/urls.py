from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory_app.urls')),  # Change 'inventory_app' to your app's name if different
]
