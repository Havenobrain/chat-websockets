from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str(self):
        return f"{str(self.room)} - {self.sender}"


class Profile(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
def __str__(self):
    return str(self.user)