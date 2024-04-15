from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users_messages.urls')),
    path('api/v1/auth/', include('authentication.urls')),
]
