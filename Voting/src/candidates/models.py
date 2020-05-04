from django.db import models
from django.db.models import Q
#from parties.models import party
# Create your models here.

class candidateQuerySet(models.query.QuerySet):
	def search(self,query):
		lookup=Q(location__icontains=query)
		return self.filter(lookup).distinct()

class candidateManager(models.Manager):
	def get_queryset(self):
		return candidateQuerySet(self.model,using=self.db)
	def search(self,query):
		return self.get_queryset().search(query)

class candidate(models.Model):
	cname=models.CharField(max_length=120,blank=True,null=True)
	location=models.CharField(max_length=50,blank=True,null=True)
	affiliation=models.ForeignKey('parties.party',on_delete=models.CASCADE,blank=True,null=True)
	#vote=models.IntegerField(default=0)
	objects=candidateManager()

	def __str__(self):
		return str(self.cname)