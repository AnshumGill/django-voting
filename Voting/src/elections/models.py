from django.db import models
from candidates.models import candidate
from django.utils import timezone
# Create your models here.
class election(models.Model):
    status=models.BooleanField(null=False,default=False)
    created=models.DateTimeField(auto_now=False,auto_now_add=True)
    candidates=models.ManyToManyField(candidate)
    start=models.DateTimeField(auto_now_add=False,auto_now=False)
    end=models.DateTimeField(auto_now_add=False,auto_now=False)

    def check_status(self):
        start=self.start
        end=self.end
        if(timezone.now()>start and timezone.now()<end):
            self.status=True
        else:
            self.status=False
        self.save()
    
    def get_status(self):
        self.check_status()
        return self.status
    
