from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    orgname = models.CharField(max_length=50, blank=True, verbose_name="Organization Name")
    pnumber = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    descrip = models.TextField(verbose_name="Description")
