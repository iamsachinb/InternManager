from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
import os
from django.core.files.storage import get_storage_class

GoogleDriveStorage = get_storage_class('django_googledrive.storage.GoogleDriveStorage')
gd_storage = GoogleDriveStorage()

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
    certificate = models.FileField(upload_to='certificate/', storage=gd_storage,  validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    permission = models.FileField(upload_to='permission/', storage=gd_storage, validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    report = models.FileField(upload_to='report/', storage=gd_storage, validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    creditsrewarded = models.IntegerField(default=0)
    submissiondate = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def delete(self, *args, **kwargs):
        # Delete associated files from Google Cloud Storage before deleting the Intern instance
        if self.certificate:
            gd_storage.delete(self.certificate.name)
        if self.permission:
            gd_storage.delete(self.permission.name)
        if self.report:
            gd_storage.delete(self.report.name)

        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)


