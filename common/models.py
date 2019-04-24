from django.db import models

from common.constants import MessageTypes


class Message(models.Model):
    """
    Model to keep messages to be displayed to users
    """

    MESSAGE_TYPE_CHOICES = (
        (MessageTypes.INFO, 'Info'),
        (MessageTypes.SUCCESS, 'Success'),
        (MessageTypes.WARNING, 'Warning'),
        (MessageTypes.ERROR, 'Error'),
    )

    key = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default=MessageTypes.ERROR)
    body = models.TextField()

    def __unicode__(self):
        return self.key
