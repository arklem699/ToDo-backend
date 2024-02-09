from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE, db_column='user_id')
    date_completion = models.DateField(blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    status_id = models.ForeignKey('app.Status', models.CASCADE, db_column='status_id')

    class Meta:
        managed = True
        db_table = 'todo'


class Status(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'