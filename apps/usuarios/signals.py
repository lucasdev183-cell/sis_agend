"""
Signals for usuarios app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, PerfilUsuario


@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a user profile when a new user is created.
    """
    if created:
        PerfilUsuario.objects.create(usuario=instance)


@receiver(post_save, sender=Usuario)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the user profile when the user is saved.
    """
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
    else:
        PerfilUsuario.objects.create(usuario=instance)