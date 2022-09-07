from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


User = get_user_model()

def set_random_url(sender, instance, created, **kwargs):
    if created:
        instance.rand_text = get_random_string(length=16)
        instance.save()
        print('signal run completed')


post_save.connect(set_random_url, sender=User)