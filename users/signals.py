from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile, Intern
from django.contrib.auth.models import User



def internAcceptedOrRejected(sender, instance, created, **kwargs):
    intern = instance
    profile = intern.owner
    if created == False:

        if intern.accepted:
            subject = "Intern Acceptance"
            message = "Dear " + profile.name + ",\n" + "Your intern " + intern.name + " have been accepted and " + str(intern.creditsrewarded) + " credit has been awarded." 

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently = False,
            )
        else:
            subject = "Intern Rejected"
            message = "Dear " + profile.name + ",\n" + "Your intern " + intern.name + " have been rejected." 

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently = False,
            )




def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()




post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(internAcceptedOrRejected, sender=Intern)















