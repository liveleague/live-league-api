from django.urls import path

from league import views

app_name = 'league'

urlpatterns = [
    path('create/venue/', views.CreateVenueView.as_view(), name='create-venue'),
    path('create/event/', views.CreateEventView.as_view(), name='create-event'),
    path('create/tally/', views.CreateTallyView.as_view(), name='create-tally'),
    path(
        'create/ticket-type/',
        views.CreateTicketTypeView.as_view(),
        name='create-ticket-type'
    ),
    path(
        'create/ticket/',
        views.CreateTicketView.as_view(),
        name='create-ticket'
    ),
    path(
        'edit/venue/<slug>/', views.EditVenueView.as_view(), name='edit-venue'
    ),
    path('edit/event/<pk>/', views.EditEventView.as_view(), name='edit-event'),
    path(
        'delete/tally/<slug>/',
        views.DeleteTallyView.as_view(),
        name='delete-tally'
    ),
    path(
        'edit/ticket-type/<slug>/',
        views.EditTicketTypeView.as_view(),
        name='edit-ticket-type'
    ),
    path(
        'vote/ticket/<pk>/', views.VoteTicketView.as_view(), name='vote'
    ),
    path('venue/<slug>/', views.RetrieveVenueView.as_view(), name='venue'),
    path('event/<pk>/', views.RetrieveEventView.as_view(), name='event'),
    path('tally/<slug>/', views.RetrieveTallyView.as_view(), name='tally'),
    path('ticket/<pk>/', views.RetrieveTicketView.as_view(), name='ticket'),
    path(
        'table-row/<slug>/',
        views.RetrieveTableRowView.as_view(),
        name='table-row'
    ),
    path(
        'list/venues/', views.ListVenueView.as_view(), name='list-venues'
    ),
    path(
        'list/events/', views.ListEventView.as_view(), name='list-events'
    ),
    path(
        'list/tallies/', views.ListTallyView.as_view(), name='list-tallies'
    ),
    path(
        'list/ticket-types/',
        views.ListTicketTypeView.as_view(),
        name='list-ticket-types'
    ),
    path(
        'list/tickets/', views.ListTicketView.as_view(), name='list-tickets'
    ),
    path(
        'list/table-rows/',
        views.ListTableRowView.as_view(),
        name='list-table-rows'
    ),
]
