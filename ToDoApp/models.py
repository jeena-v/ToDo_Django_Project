from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    title =models.CharField(max_length=200)
    description =models.TextField(blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.title
    


