from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<version>/user/', include('user.doc_urls')),
    path('<version>/league/', include('league.doc_urls')),
]
