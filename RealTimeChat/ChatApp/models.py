from django.db import models

class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    
    def return_room_messages(self):

        return Message.objects.filter(room=self)
    
    def create_new_room_message(self, sender,senderName, message):

        new_message = Message(room=self, sender=sender,senderName=senderName, message=message)
        new_message.save()

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    senderName = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)
    
class PrivateChat(models.Model):
    chat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.chat_name
    
    def return_room_messages(self):

        return PrivateMessage.objects.filter(receiver=self)
    
    def create_new_room_message(receiver, sender, message):

        new_message = PrivateMessage(receiver=receiver, sender=sender, message=message)
        new_message.save()    
    
class PrivateMessage(models.Model):
    privateChat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    message = models.TextField()
