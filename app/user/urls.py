from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path(
        'create/artist/',
        views.CreateArtistView.as_view(),
        name='create-artist'
    ),
    path(
        'create/promoter/',
        views.CreatePromoterView.as_view(),
        name='create-promoter'
    ),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
