from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Post, Log


@receiver(post_save, sender=Post)
def log_post_creation(sender, instance, created, **kwargs):
    # print('signal in')
    if created:
        log = Log.objects.create(
            action=f'Post "{instance.title}" created',
            description=f'New post "{instance.title}" was created with id {instance.id}',
        )
        log.save()
        # print('signal out')


@receiver(post_save, sender=User)
def log_advuser_creation(sender, instance, created, **kwargs):
    if created:
        log = Log.objects.create(
            action=f'User "{instance.username}" created',
            description=f'New User "{instance.username}" was created with id {instance.id} amd email {instance.email}',
        )
        log.save()

