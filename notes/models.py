from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Note(models.Model):
    title = models.CharField(max_length=100,default='Untitled')
    content = models.TextField(default='Not added...')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    shared_users = models.ManyToManyField(User, related_name='shared_notes')
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

# also can add as need like user_track | changed_by and so on
    
    def __str__(self):
        return self.title