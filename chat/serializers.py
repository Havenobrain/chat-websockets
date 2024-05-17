from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializer.CurrentUserDefault())

    class Meta:
        model = Room
        fields = ('room_name', 'user')



