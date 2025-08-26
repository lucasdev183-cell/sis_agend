"""
Employee models for JT Sistemas.
"""
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Cargo(BaseModel):
    """
    Model for employee positions/roles.
    """
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome do Cargo'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição detalhada das responsabilidades do cargo'
    )
    salario_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salário Base',
        help_text='Salário base para este cargo'
    )
    nivel_hierarquico = models.PositiveIntegerField(
        default=1,
        verbose_name='Nível Hierárquico',
        help_text='1 = Mais alto, números maiores = níveis mais baixos'
    )
    cor_identificacao = models.CharField(
        max_length=7,
        default='#007bff',
        verbose_name='Cor de Identificação',
        help_text='Cor hexadecimal para identificação visual'
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nivel_hierarquico', 'nome']

    def __str__(self):
        return self.nome

    @property
    def total_funcionarios(self):
        """Return the total number of employees in this position"""
        return self.funcionarios.filter(is_active=True).count()


class Funcionario(BaseModel):
    """
    Model for employees.
    """
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('ferias', 'Férias'),
        ('licenca', 'Licença'),
        ('demitido', 'Demitido'),
    ]

    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
        ('plantao', 'Plantão'),
    ]

    # Basic Information
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome Completo'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone',
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

    # Personal Information
    cpf = models.CharField(
        max_length=14,
        unique=True,
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
        verbose_name='Data de Nascimento'
    )
    endereco = models.CharField(
        max_length=200,
        verbose_name='Endereço'
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name='Cidade'
    )
    estado = models.CharField(
        max_length=2,
        verbose_name='Estado'
    )
    cep = models.CharField(
        max_length=9,
        verbose_name='CEP',
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message="CEP deve estar no formato: 00000-000"
            ),
        ]
    )

    # Professional Information
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name='funcionarios',
        verbose_name='Cargo'
    )
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionario',
        verbose_name='Usuário do Sistema',
        help_text='Vinculação com usuário do sistema (opcional)'
    )
    matricula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Matrícula'
    )
    data_admissao = models.DateField(
        verbose_name='Data de Admissão'
    )
    data_demissao = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Demissão'
    )
    salario_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Atual'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name='Status'
    )
    turno = models.CharField(
        max_length=20,
        choices=TURNO_CHOICES,
        default='integral',
        verbose_name='Turno de Trabalho'
    )

    # Work Schedule
    horario_entrada = models.TimeField(
        verbose_name='Horário de Entrada'
    )
    horario_saida = models.TimeField(
        verbose_name='Horário de Saída'
    )
    dias_trabalho = models.CharField(
        max_length=20,
        default='seg-sex',
        verbose_name='Dias de Trabalho',
        help_text='Ex: seg-sex, seg-sab, etc.'
    )

    # Additional Information
    foto = models.ImageField(
        upload_to='funcionarios/fotos/',
        blank=True,
        null=True,
        verbose_name='Foto'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    especialidades = models.TextField(
        blank=True,
        verbose_name='Especialidades',
        help_text='Especialidades ou habilidades específicas'
    )

    # Emergency Contact
    contato_emergencia_nome = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nome do Contato de Emergência'
    )
    contato_emergencia_telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone do Contato de Emergência'
    )
    contato_emergencia_parentesco = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Parentesco do Contato de Emergência'
    )

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['cargo']),
            models.Index(fields=['matricula']),
            models.Index(fields=['cpf']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.cargo.nome}"

    def save(self, *args, **kwargs):
        # Generate matricula if not provided
        if not self.matricula:
            from django.utils import timezone
            year = timezone.now().year
            last_funcionario = Funcionario.objects.filter(
                matricula__startswith=str(year)
            ).order_by('-matricula').first()
            
            if last_funcionario:
                last_number = int(last_funcionario.matricula[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.matricula = f"{year}{new_number:04d}"
        
        super().save(*args, **kwargs)

    @property
    def nome_display(self):
        """Return the display name"""
        return self.nome

    @property
    def endereco_completo(self):
        """Return full address as a string"""
        parts = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([part for part in parts if part])

    @property
    def idade(self):
        """Calculate and return employee's age"""
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            return today.year - self.data_nascimento.year - (
                (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None

    @property
    def tempo_empresa(self):
        """Calculate time working at the company"""
        if self.data_admissao:
            from datetime import date
            end_date = self.data_demissao if self.data_demissao else date.today()
            delta = end_date - self.data_admissao
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return {'years': years, 'months': months, 'total_days': delta.days}
        return None

    @property
    def is_ativo(self):
        """Check if employee is active"""
        return self.status == 'ativo' and self.is_active

    @property
    def contato_emergencia_completo(self):
        """Return complete emergency contact info"""
        if self.contato_emergencia_nome:
            parts = [self.contato_emergencia_nome]
            if self.contato_emergencia_parentesco:
                parts.append(f"({self.contato_emergencia_parentesco})")
            if self.contato_emergencia_telefone:
                parts.append(f"- {self.contato_emergencia_telefone}")
            return ' '.join(parts)
        return None

    def get_agendamentos_hoje(self):
        """Get today's appointments for this employee"""
        from datetime import date
        from apps.agendamentos.models import Agendamento
        
        return Agendamento.objects.filter(
            funcionario=self,
            data_hora__date=date.today(),
            is_active=True
        ).exclude(status='cancelado')

    def get_total_agendamentos_mes(self, mes=None, ano=None):
        """Get total appointments for a specific month"""
        from datetime import date
        from apps.agendamentos.models import Agendamento
        
        if not mes:
            mes = date.today().month
        if not ano:
            ano = date.today().year
            
        return Agendamento.objects.filter(
            funcionario=self,
            data_hora__month=mes,
            data_hora__year=ano,
            is_active=True
        ).exclude(status='cancelado').count()


class HistoricoSalario(BaseModel):
    """
    Model to track salary history for employees.
    """
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='historico_salarios',
        verbose_name='Funcionário'
    )
    salario_anterior = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Anterior'
    )
    salario_novo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Novo'
    )
    data_alteracao = models.DateField(
        verbose_name='Data da Alteração'
    )
    motivo = models.TextField(
        blank=True,
        verbose_name='Motivo da Alteração'
    )
    usuario_responsavel = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário Responsável'
    )

    class Meta:
        verbose_name = 'Histórico de Salário'
        verbose_name_plural = 'Históricos de Salário'
        ordering = ['-data_alteracao']

    def __str__(self):
        return f"{self.funcionario.nome} - {self.data_alteracao}"

    @property
    def percentual_aumento(self):
        """Calculate percentage increase"""
        if self.salario_anterior > 0:
            return ((self.salario_novo - self.salario_anterior) / self.salario_anterior) * 100
        return 0

    @property
    def valor_aumento(self):
        """Calculate absolute increase value"""
        return self.salario_novo - self.salario_anterior