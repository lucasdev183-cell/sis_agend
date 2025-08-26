"""
User models for JT Sistemas.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import TimestampedModel


class Usuario(AbstractUser, TimestampedModel):
    """
    Custom User model extending Django's AbstractUser.
    Includes business-specific fields and permissions.
    """
    TIPO_CHOICES = [
        ('master', 'Master'),
        ('restrito', 'Restrito'),
    ]

    # Basic Information
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome Completo'
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
            ),
        ]
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='restrito',
        verbose_name='Tipo de Usuário'
    )
    
    # Avatar/Profile Picture
    avatar = models.ImageField(
        upload_to='usuarios/avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    
    # Business Permissions
    pode_cadastrar_cliente = models.BooleanField(
        default=False,
        verbose_name='Pode Cadastrar Cliente',
        help_text='Permite ao usuário cadastrar novos clientes'
    )
    pode_cadastrar_funcionario = models.BooleanField(
        default=False,
        verbose_name='Pode Cadastrar Funcionário',
        help_text='Permite ao usuário cadastrar novos funcionários'
    )
    pode_cadastrar_cargo = models.BooleanField(
        default=False,
        verbose_name='Pode Cadastrar Cargo',
        help_text='Permite ao usuário criar novos cargos'
    )
    pode_agendar = models.BooleanField(
        default=True,
        verbose_name='Pode Agendar',
        help_text='Permite ao usuário criar agendamentos'
    )
    pode_ver_agendamentos = models.BooleanField(
        default=True,
        verbose_name='Pode Ver Agendamentos',
        help_text='Permite ao usuário visualizar agendamentos'
    )
    pode_editar_agendamentos = models.BooleanField(
        default=False,
        verbose_name='Pode Editar Agendamentos',
        help_text='Permite ao usuário editar agendamentos'
    )
    pode_cancelar_agendamentos = models.BooleanField(
        default=False,
        verbose_name='Pode Cancelar Agendamentos',
        help_text='Permite ao usuário cancelar agendamentos'
    )
    pode_ver_relatorios = models.BooleanField(
        default=False,
        verbose_name='Pode Ver Relatórios',
        help_text='Permite ao usuário acessar relatórios'
    )
    pode_gerenciar_configuracoes = models.BooleanField(
        default=False,
        verbose_name='Pode Gerenciar Configurações',
        help_text='Permite ao usuário alterar configurações do sistema'
    )
    
    # Activity tracking
    ultimo_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Último IP de Login'
    )
    tentativas_login = models.PositiveIntegerField(
        default=0,
        verbose_name='Tentativas de Login Falhadas'
    )
    conta_bloqueada_ate = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Conta Bloqueada Até'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome', 'username']
        indexes = [
            models.Index(fields=['tipo_usuario']),
            models.Index(fields=['is_active']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.username})"

    def save(self, *args, **kwargs):
        # Set master permissions automatically
        if self.tipo_usuario == 'master':
            self.is_staff = True
            self.is_superuser = True
            self.pode_cadastrar_cliente = True
            self.pode_cadastrar_funcionario = True
            self.pode_cadastrar_cargo = True
            self.pode_agendar = True
            self.pode_ver_agendamentos = True
            self.pode_editar_agendamentos = True
            self.pode_cancelar_agendamentos = True
            self.pode_ver_relatorios = True
            self.pode_gerenciar_configuracoes = True
        super().save(*args, **kwargs)

    @property
    def nome_display(self):
        """Return the display name (nome if available, otherwise username)"""
        return self.nome if self.nome else self.username

    @property
    def is_master(self):
        """Check if user is a master user"""
        return self.tipo_usuario == 'master'

    @property
    def is_restrito(self):
        """Check if user is a restricted user"""
        return self.tipo_usuario == 'restrito'

    def has_permission(self, permission_name):
        """Check if user has a specific business permission"""
        if self.is_master:
            return True
        return getattr(self, permission_name, False)

    def get_permissions_list(self):
        """Get list of all permissions for this user"""
        permissions = []
        permission_fields = [
            'pode_cadastrar_cliente',
            'pode_cadastrar_funcionario',
            'pode_cadastrar_cargo',
            'pode_agendar',
            'pode_ver_agendamentos',
            'pode_editar_agendamentos',
            'pode_cancelar_agendamentos',
            'pode_ver_relatorios',
            'pode_gerenciar_configuracoes',
        ]
        
        for field in permission_fields:
            if getattr(self, field):
                permissions.append(field)
        
        return permissions

    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter"""
        self.tentativas_login = 0
        self.conta_bloqueada_ate = None
        self.save(update_fields=['tentativas_login', 'conta_bloqueada_ate'])

    def increment_failed_login_attempts(self):
        """Increment failed login attempts and potentially block account"""
        from django.utils import timezone
        from datetime import timedelta
        
        self.tentativas_login += 1
        
        # Block account after 5 failed attempts for 30 minutes
        if self.tentativas_login >= 5:
            self.conta_bloqueada_ate = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['tentativas_login', 'conta_bloqueada_ate'])

    @property
    def is_account_locked(self):
        """Check if account is currently locked"""
        from django.utils import timezone
        
        if self.conta_bloqueada_ate:
            return timezone.now() < self.conta_bloqueada_ate
        return False


class PerfilUsuario(TimestampedModel):
    """
    Extended user profile information.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuário'
    )
    
    # Additional personal information
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Nascimento'
    )
    cpf = models.CharField(
        max_length=14,
        blank=True,
        verbose_name='CPF',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="CPF deve estar no formato: 000.000.000-00"
            ),
        ]
    )
    endereco = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Endereço'
    )
    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cidade'
    )
    estado = models.CharField(
        max_length=2,
        blank=True,
        verbose_name='Estado'
    )
    cep = models.CharField(
        max_length=9,
        blank=True,
        verbose_name='CEP',
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message="CEP deve estar no formato: 00000-000"
            ),
        ]
    )
    
    # Professional information
    cargo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cargo'
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Departamento'
    )
    data_admissao = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Admissão'
    )
    
    # Preferences
    tema_preferido = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Claro'),
            ('dark', 'Escuro'),
            ('auto', 'Automático'),
        ],
        default='light',
        verbose_name='Tema Preferido'
    )
    idioma = models.CharField(
        max_length=10,
        choices=[
            ('pt-br', 'Português (Brasil)'),
            ('en', 'English'),
            ('es', 'Español'),
        ],
        default='pt-br',
        verbose_name='Idioma'
    )
    receber_notificacoes_email = models.BooleanField(
        default=True,
        verbose_name='Receber Notificações por Email'
    )
    receber_notificacoes_whatsapp = models.BooleanField(
        default=False,
        verbose_name='Receber Notificações por WhatsApp'
    )

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'

    def __str__(self):
        return f"Perfil de {self.usuario.nome_display}"

    @property
    def endereco_completo(self):
        """Return full address as a string"""
        parts = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([part for part in parts if part])

    @property
    def idade(self):
        """Calculate and return user's age"""
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            return today.year - self.data_nascimento.year - (
                (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None