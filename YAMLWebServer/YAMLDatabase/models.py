from django.db import models

# Create your models here.


class Filename(models.Model):
    filename = models.CharField(max_length = 100, unique=True, null = True)
    def __str__(self):
        return self.filename


class YAMLEntry(models.Model):
    filename = models.ForeignKey(Filename, null = True, on_delete = models.CASCADE)

    hostname = models.CharField(max_length = 100, null = True)
    host = models.CharField(max_length = 100, null=True, blank = True)
    username = models.CharField(max_length = 100, null=True, blank = True)
    password = models.CharField(max_length = 100, null=True, blank = True)
    device_type = models.CharField(max_length = 100, null=True, blank = True)

    class Meta():
        unique_together = ('filename','hostname',)
    def __str__(self):
        return self.hostname







