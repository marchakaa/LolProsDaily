from django.db import models

# Player model.
class Player(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    current_team = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name