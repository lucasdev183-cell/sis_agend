"""
Client models for JT Sistemas.
"""
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Cliente(BaseModel):
    """
    Model for clients/customers.
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Não informar'),
    ]

    TIPO_CLIENTE_CHOICES = [
        ('pessoa_fisica', 'Pessoa Física'),
        ('pessoa_juridica', 'Pessoa Jurídica'),
    ]

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('bloqueado', 'Bloqueado'),
        ('vip', 'VIP'),
    ]

    # Basic Information
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome/Razão Social'
    )
    nome_fantasia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nome Fantasia',
        help_text='Para pessoa jurídica'
    )
    tipo_cliente = models.CharField(
        max_length=20,
        choices=TIPO_CLIENTE_CHOICES,
        default='pessoa_fisica',
        verbose_name='Tipo de Cliente'
    )
    
    # Contact Information
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone Principal',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
            ),
        ]
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='WhatsApp',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de WhatsApp deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
            ),
        ]
    )
    telefone_secundario = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone Secundário',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
            ),
        ]
    )

    # Personal Information (for Pessoa Física)
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
    rg = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='RG'
    )
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Nascimento'
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        verbose_name='Sexo'
    )

    # Business Information (for Pessoa Jurídica)
    cnpj = models.CharField(
        max_length=18,
        blank=True,
        verbose_name='CNPJ',
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message="CNPJ deve estar no formato: 00.000.000/0000-00"
            ),
        ]
    )
    inscricao_estadual = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Inscrição Estadual'
    )
    inscricao_municipal = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Inscrição Municipal'
    )

    # Address Information
    endereco = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Endereço'
    )
    numero = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Número'
    )
    complemento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Complemento'
    )
    bairro = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Bairro'
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

    # Business Information
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name='Status'
    )
    data_primeiro_atendimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Primeiro Atendimento'
    )
    data_ultimo_atendimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Último Atendimento'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    preferencias = models.TextField(
        blank=True,
        verbose_name='Preferências',
        help_text='Preferências específicas do cliente'
    )
    
    # Marketing and Communication
    como_conheceu = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Como Conheceu a Empresa',
        help_text='Indicação, internet, propaganda, etc.'
    )
    aceita_marketing = models.BooleanField(
        default=True,
        verbose_name='Aceita Receber Marketing',
        help_text='Aceita receber promoções e novidades'
    )
    aceita_whatsapp = models.BooleanField(
        default=True,
        verbose_name='Aceita WhatsApp',
        help_text='Aceita receber mensagens via WhatsApp'
    )

    # Photo
    foto = models.ImageField(
        upload_to='clientes/fotos/',
        blank=True,
        null=True,
        verbose_name='Foto'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['tipo_cliente']),
            models.Index(fields=['cpf']),
            models.Index(fields=['cnpj']),
            models.Index(fields=['telefone']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Set first appointment date if not set
        if not self.data_primeiro_atendimento:
            from django.utils import timezone
            self.data_primeiro_atendimento = timezone.now()
        
        super().save(*args, **kwargs)

    @property
    def nome_display(self):
        """Return the display name"""
        if self.nome_fantasia and self.tipo_cliente == 'pessoa_juridica':
            return f"{self.nome_fantasia} ({self.nome})"
        return self.nome

    @property
    def endereco_completo(self):
        """Return full address as a string"""
        parts = []
        if self.endereco:
            endereco_base = self.endereco
            if self.numero:
                endereco_base += f", {self.numero}"
            if self.complemento:
                endereco_base += f", {self.complemento}"
            parts.append(endereco_base)
        
        if self.bairro:
            parts.append(self.bairro)
        if self.cidade:
            parts.append(self.cidade)
        if self.estado:
            parts.append(self.estado)
        if self.cep:
            parts.append(self.cep)
        
        return ' - '.join([part for part in parts if part])

    @property
    def documento_principal(self):
        """Return the main document (CPF or CNPJ)"""
        if self.tipo_cliente == 'pessoa_fisica':
            return self.cpf
        else:
            return self.cnpj

    @property
    def idade(self):
        """Calculate and return client's age"""
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            return today.year - self.data_nascimento.year - (
                (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None

    @property
    def tempo_cliente(self):
        """Calculate how long the person has been a client"""
        if self.data_primeiro_atendimento:
            from django.utils import timezone
            delta = timezone.now() - self.data_primeiro_atendimento
            return delta.days
        return 0

    @property
    def is_ativo(self):
        """Check if client is active"""
        return self.status == 'ativo' and self.is_active

    @property
    def is_vip(self):
        """Check if client is VIP"""
        return self.status == 'vip'

    def get_total_agendamentos(self):
        """Get total number of appointments"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            cliente=self,
            is_active=True
        ).count()

    def get_agendamentos_concluidos(self):
        """Get total number of completed appointments"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            cliente=self,
            status='concluido',
            is_active=True
        ).count()

    def get_agendamentos_cancelados(self):
        """Get total number of cancelled appointments"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            cliente=self,
            status='cancelado',
            is_active=True
        ).count()

    def get_ultimo_agendamento(self):
        """Get the last appointment"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            cliente=self,
            is_active=True
        ).order_by('-data_hora').first()

    def get_proximo_agendamento(self):
        """Get the next appointment"""
        from django.utils import timezone
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            cliente=self,
            data_hora__gte=timezone.now(),
            is_active=True
        ).exclude(status='cancelado').order_by('data_hora').first()

    def atualizar_ultimo_atendimento(self):
        """Update the last service date"""
        from django.utils import timezone
        self.data_ultimo_atendimento = timezone.now()
        self.save(update_fields=['data_ultimo_atendimento'])

    def get_servicos_favoritos(self, limit=5):
        """Get client's favorite services based on appointment history"""
        from django.db.models import Count
        from apps.agendamentos.models import Agendamento
        
        return Agendamento.objects.filter(
            cliente=self,
            status='concluido',
            is_active=True
        ).values(
            'servico__nome'
        ).annotate(
            total=Count('servico')
        ).order_by('-total')[:limit]


class HistoricoContato(BaseModel):
    """
    Model to track communication history with clients.
    """
    TIPO_CONTATO_CHOICES = [
        ('telefone', 'Telefone'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('presencial', 'Presencial'),
        ('sms', 'SMS'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='historico_contatos',
        verbose_name='Cliente'
    )
    tipo_contato = models.CharField(
        max_length=20,
        choices=TIPO_CONTATO_CHOICES,
        verbose_name='Tipo de Contato'
    )
    assunto = models.CharField(
        max_length=200,
        verbose_name='Assunto'
    )
    descricao = models.TextField(
        verbose_name='Descrição do Contato'
    )
    data_contato = models.DateTimeField(
        verbose_name='Data/Hora do Contato'
    )
    usuario_responsavel = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário Responsável'
    )
    anexos = models.FileField(
        upload_to='clientes/contatos/',
        blank=True,
        null=True,
        verbose_name='Anexos'
    )

    class Meta:
        verbose_name = 'Histórico de Contato'
        verbose_name_plural = 'Históricos de Contato'
        ordering = ['-data_contato']

    def __str__(self):
        return f"{self.cliente.nome} - {self.assunto} ({self.data_contato})"