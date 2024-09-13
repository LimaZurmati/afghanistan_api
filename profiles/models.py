from django.db import models


class Profile(models.Model):
    """
    Profile model, related to User
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    image = models.ImageField(
    upload_to='images/', default='../default_profile_te45n4'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"



