from django.db import models
from consumer.models import CustomUser, BaseModel

class Duo(BaseModel):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        abstract = True

class DuoMessage(Duo):
    message = models.TextField()

    def __str__(self):
        return f'Message from {self.sender.name} to {self.receiver.name}'

class DuoFile(Duo):
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'File from {self.sender.name} to {self.receiver.name}'