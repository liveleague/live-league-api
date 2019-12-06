"""app URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer

schema_view = get_schema_view(
    title='Testing API',
    url='https://www.example.org/api/',
    renderer_classes=[JSONOpenAPIRenderer]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<version>/league/', include('league.urls')),
    path('<version>/user/', include('user.urls')),
    path('<version>/superuser/', include('superuser.urls')),
    path('schema.json', schema_view),    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
