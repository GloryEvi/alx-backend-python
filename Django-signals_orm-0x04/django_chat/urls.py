from django.urls import path
from . import views

urlpatterns = [
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
    path('delete-account/', views.delete_user, name='delete_user'),
    path('threaded/', views.threaded_messages, name='threaded_messages'),
    path('inbox/unread/', views.unread_inbox, name='unread_inbox'),
]