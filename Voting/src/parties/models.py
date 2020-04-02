from django.db import models
from candidates.models import candidate
# Create your models here.
class party(models.Model):
	pname=models.CharField(max_length=120)
	members=models.ManyToManyField(candidate,blank=True)
	
	def __str__(self):
		return str(self.pname)	