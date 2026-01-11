"""
URL configuration for pylearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# In your project's urls.py
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from core.sitemap import PostSitemap

sitemaps = {
    'communityposts': PostSitemap,  # Register your sitemaps here
}



urlpatterns = [
    path('pylearnhub-admin/', admin.site.urls),
path('', include('core.urls')),
path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns = urlpatterns+static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
