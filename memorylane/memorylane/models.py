from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=5000) 
    friends = models.CharField(max_length=5000)
    date_created = models.DateField()
    bio = models.TextField(default="Default bio")
    livesin = models.TextField(default="Earth")
    about = models.TextField()
    memories = models.CharField(max_length=5000)
    propic = models.FileField(upload_to="memorylane/static/images/profile")
    image = models.FileField(upload_to="memorylane/static/user-images", default="memorylane/static/user-images/Default.png")

    def __str__(self):
        return self.first_name + " " + self.last_name

class Memory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.FileField(upload_to="memorylane/static/images")
    author_image = models.FileField(default="memorylane/static/user-images/Default.png")
    first_name = models.CharField(max_length=100, default="Memory")
    last_name = models.CharField(max_length=100, default="Lane")
    description = models.TextField()
    author = models.CharField(max_length=100)
    date_created = models.DateField()

    def __str__(self):
    	return self.name