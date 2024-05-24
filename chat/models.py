from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='rooms', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str(self):
        return f"{str(self.room)} - {self.sender}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(Room, related_name='members')
    name=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
def __str__(self):
    return str(self.user)