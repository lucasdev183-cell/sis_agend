"""
Core models for JT Sistemas.
Contains abstract base models and utility classes.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract base class that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base class that provides soft delete functionality.
    """
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Excluído em')

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the object"""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore the soft deleted object"""
        self.is_active = True
        self.deleted_at = None
        self.save()


class BaseModel(TimestampedModel, SoftDeleteModel):
    """
    Abstract base model that combines timestamp and soft delete functionality.
    """
    class Meta:
        abstract = True


class AuditLog(models.Model):
    """
    Model to track user actions for auditing purposes.
    """
    ACTION_CHOICES = [
        ('create', 'Criação'),
        ('update', 'Atualização'),
        ('delete', 'Exclusão'),
        ('view', 'Visualização'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='audit_logs'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Ação'
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name='Nome do Modelo',
        help_text='Nome do modelo que foi afetado'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID do Objeto'
    )
    object_repr = models.CharField(
        max_length=200,
        verbose_name='Representação do Objeto'
    )
    changes = models.JSONField(
        default=dict,
        verbose_name='Alterações',
        help_text='Detalhes das alterações realizadas'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Endereço IP'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora'
    )

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['model_name', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name} ({self.timestamp})"


class SystemConfiguration(models.Model):
    """
    Model to store system-wide configuration settings.
    """
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Chave'
    )
    value = models.TextField(
        verbose_name='Valor'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descrição'
    )
    is_sensitive = models.BooleanField(
        default=False,
        verbose_name='Sensível',
        help_text='Indica se o valor contém informações sensíveis'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.description or 'Sem descrição'}"

    @classmethod
    def get_value(cls, key, default=None):
        """Get configuration value by key"""
        try:
            config = cls.objects.get(key=key)
            return config.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, key, value, description=''):
        """Set configuration value"""
        config, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            config.value = value
            if description:
                config.description = description
            config.save()
        return config