from django.db import models
from django.conf import settings

class MessageModel(models.Model):
    """
    Model representing a message.
    """
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='username',
        related_name='sender'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='username',
        related_name='receiver'
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    unread = models.BooleanField(default=True, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sender', 'creation_date']