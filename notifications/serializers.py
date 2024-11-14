from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    action_user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = '__all__'