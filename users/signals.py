from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import send_sms
from django.contrib.auth import get_user_model


user = get_user_model()

@receiver(user_logged_in, sender=user)
def post_login(sender, user, request, **kwargs):
    pass
    # send_sms([user.phone_number], 'You Entered BCM Crisis Software')