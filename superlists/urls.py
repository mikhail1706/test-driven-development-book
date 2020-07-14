"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from lists import views
from django.conf import settings
from django.conf.urls.static import static
from lists.api import router

urlpatterns = [
                  url(r'^$', views.HomePageView.as_view(), name='home_page'),
                  url(r'^lists/', include('lists.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^accounts/', include('accounts.urls')),
                  # url(r'^api/', include('lists.api_urls')),
                  url(r'^api/', include(router.urls)),

              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
