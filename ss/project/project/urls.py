"""
URL configuration for project project.

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
from django.urls import path,include
from django.conf.urls.static import static
from . import settings
from accounts.views import LoginView , UserDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('accounts/', include('accounts.urls')),
    #path('accounts/user-details/', UserDetailView.as_view(), name='user-details'),
    #path('customer/', include('customer.urls')),
    #path('service-provider/', include('serviceprovider.urls')),
    path('dealer/', include('dealer.urls')),
    path('franchise/',include('franchise.urls')),
    path("adminapp/", include("adminapp.urls")), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

