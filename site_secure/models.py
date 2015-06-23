from django.db import models
from django.contrib.auth.models import User
from time import time

# Create your models here.

def get_upload_file_name(instance, filename):
	return 'uploaded_files/%s_%s' % (str(time()).replace('.','_'), filename)

class file_folder(models.Model):
	title = models.CharField(max_length = 30, unique = True)
	user = models.ForeignKey(User)
	File = models.FileField(upload_to = get_upload_file_name)