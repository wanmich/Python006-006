from django.db import models

# Create your models here.


class ShortComments(models.Model):
    stars = models.IntegerField()
    comment = models.CharField(max_length=500)
    comment_date = models.CharField(max_length=20)
    cid = models.IntegerField()
