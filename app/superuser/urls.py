from django.urls import path

from superuser import views

app_name = 'superuser'

urlpatterns = [
    path('credit/<pk>', views.ManageCreditView.as_view(), name='credit'),
]
