from django.db import models

# Create your models here.
class vote(models.Model):
	cname=models.CharField(max_length=120)
	vname=models.CharField(max_length=120)
	tx_hash=models.CharField(max_length=200)
	block_hash=models.CharField(max_length=200)
	
