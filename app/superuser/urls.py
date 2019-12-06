from django.urls import path

from superuser import views

app_name = 'superuser'

urlpatterns = [
    path('create/secret', views.create_secret, name='create-secret'),
    path('password/<email>', views.ManagePassword.as_view(), name='password'),
    path('credit/<pk>', views.ManageCreditView.as_view(), name='credit'),
    path('stripe/<pk>', views.ManageStripeView.as_view(), name='stripe'),
]
