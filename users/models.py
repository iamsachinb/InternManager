from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator


# Create your models here.




class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    regno = models.CharField(max_length=7, blank=True, null=True)
    creditsearned = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.regno)
    
    class Meta:
        ordering = ['regno']

class Intern(models.Model):

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    reviewed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='certificate/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    permission = models.FileField(upload_to='permission/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    report = models.FileField(upload_to='report/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    creditsrewarded = models.IntegerField(default=0)
    submissiondate = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    

    def __str__(self):
        return str(self.name)


