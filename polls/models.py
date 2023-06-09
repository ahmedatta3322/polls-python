from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone

class Poll(models.Model):

    question = models.CharField(max_length=200)
    expiration_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200 , unique=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.choice_text