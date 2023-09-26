from django.db import models
from django.contrib.auth import get_user_model

class Patient(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField(default = 0)
    rating = models.IntegerField(default = 0)
    reviewer = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)


    def __str__(self):
     return self.name


class UploadedPDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    generated_hpi = models.TextField()