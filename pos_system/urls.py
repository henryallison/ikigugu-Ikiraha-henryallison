from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('admin-login')),
    path('admin/', admin.site.urls),
    path('login/', include('products.urls')),  # handles login, dashboard, etc.
    path('dashboard/', include('products.urls')),
    path('logout/', include('products.urls')),
    path('products/', include('products.urls')),  # ✅ handles ALL product views here!
    path('', include('admin_management.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
