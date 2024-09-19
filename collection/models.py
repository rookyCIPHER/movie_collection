from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Collection(models.Model):
    title=models.CharField(max_length=100)
    uuid=models.CharField(unique=True,max_length=100)
    description=models.CharField(max_length=1000)
    user = models.ForeignKey(
        User,  
        on_delete=models.CASCADE,
        related_name='collections',
        null=True 
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("Collection must be associated with a user.")
        super().save(*args, **kwargs)


class MoviesInCollection(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,related_name='movies',null=True )
    movie_id = models.CharField(unique=True,max_length=100)  
    title = models.CharField(max_length=255)
    description=models.CharField(max_length=1000)
    genre=models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.collection:
            raise ValueError("Movie must be associated with a collection.")
        super().save(*args, **kwargs)