"""Here we define our data types"""
import datetime

from django.db import models
from django.utils import timezone


class Abstract():
    """Contains general-use methods"""

    def __str__(self):
        """Nice representation for API tool"""

        return self.text


class Question(Abstract, models.Model):
    """Contains publication date and the question itself"""
    
    text = models.CharField(max_length=200)
    dt_published = models.DateTimeField('date published')

    def is_recent(self):
        """Was question published recently? Method sed for questions sorting"""

        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.dt_published <= now

    is_recent.admin_order_field = 'dt_published'
    is_recent.boolean = True
    is_recent.short_description = 'Published recently?'


class Choice(Abstract, models.Model):
    """Contains choice text, the number of votes and references Question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
