# models.py
from django.db import models

class SelectedCollege(models.Model):
    name = models.CharField(max_length=255)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]  # Display first 50 characters in admin
