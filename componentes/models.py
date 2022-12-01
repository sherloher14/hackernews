from django.db import models
from django.conf import settings
# ...code

# Create your models here.
class Componente(models.Model):
    name= models.TextField()
    semestre = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
