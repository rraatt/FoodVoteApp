from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    """A model for restaurant. Created together with owner account by user with admin rights"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant')

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Model for containing a menu for the day, menus content is stored as text. HTML+CSS?"""
    day = models.DateField()
    content = models.TextField()
    owner = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')

    def get_count(self):
        """Get amount of votes for given menu at current time"""
        return Vote.objects.filter(menu=self.pk).filter(vote_date=timezone.now().date()).count()

    def __str__(self):
        return self.owner.name + ' ' + str(self.day)


class Vote(models.Model):
    """Model for keeping track of votes. Contains a restriction,
    so users can't vote multiple times a day"""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'vote_date')
