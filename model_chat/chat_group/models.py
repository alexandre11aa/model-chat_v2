from django.db import models
from consumer.models import CustomUser, BaseModel
   
class GroupChat(BaseModel):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, related_name='group_chats')

    def __str__(self):
        return self.name

class GroupMessage(BaseModel):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.name} in {self.group_chat.name}'