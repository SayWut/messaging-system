from django.urls import path
from .views import UserMessagesView, UserMessageView

urlpatterns = [
    path('messages', UserMessagesView.as_view(), name='user_messages'),
    path('message', UserMessageView.as_view()),
]
