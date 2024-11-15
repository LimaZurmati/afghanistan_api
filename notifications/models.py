from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Recipient
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')  # Action taker
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    object_id = models.IntegerField()  # ID of the liked post or followed user
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action_user.username} {self.notification_type} {self.user.username}"