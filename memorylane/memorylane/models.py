from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=5000) 
    friends = models.CharField(max_length=5000)
    propic = models.CharField(max_length=1000)
    date_created = models.DateField()
    bio = models.TextField()
    livesin = models.TextField()
    about = models.TextField()
    memories = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Memory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.FileField(upload_to="memorylane/static/images")
    description = models.TextField()
    author = models.CharField(max_length=100)
    date_created = models.DateField()

    def __str__(self):
    	return self.name