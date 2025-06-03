from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    User profile model that extends the default User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_person = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username