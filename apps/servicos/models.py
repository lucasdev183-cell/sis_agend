"""
Service models for JT Sistemas.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel


class CategoriaServico(BaseModel):
    """
    Model for service categories.
    """
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome da Categoria'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    cor_identificacao = models.CharField(
        max_length=7,
        default='#007bff',
        verbose_name='Cor de Identificação',
        help_text='Cor hexadecimal para identificação visual'
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Ícone',
        help_text='Nome do ícone FontAwesome (ex: fa-cut, fa-star)'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Exibição'
    )

    class Meta:
        verbose_name = 'Categoria de Serviço'
        verbose_name_plural = 'Categorias de Serviço'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

    @property
    def total_servicos(self):
        """Return the total number of services in this category"""
        return self.servicos.filter(is_active=True).count()


class Servico(BaseModel):
    """
    Model for services offered by the company.
    """
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('promocao', 'Promoção'),
        ('descontinuado', 'Descontinuado'),
    ]

    TIPO_DURACAO_CHOICES = [
        ('minutos', 'Minutos'),
        ('horas', 'Horas'),
        ('dias', 'Dias'),
    ]

    # Basic Information
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Serviço'
    )
    descricao = models.TextField(
        verbose_name='Descrição Detalhada'
    )
    descricao_curta = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descrição Resumida',
        help_text='Descrição breve para exibição em listas'
    )
    categoria = models.ForeignKey(
        CategoriaServico,
        on_delete=models.PROTECT,
        related_name='servicos',
        verbose_name='Categoria'
    )

    # Pricing
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço'
    )
    preco_promocional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Preço Promocional'
    )
    data_inicio_promocao = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Início da Promoção'
    )
    data_fim_promocao = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Fim da Promoção'
    )

    # Duration and Scheduling
    duracao = models.PositiveIntegerField(
        verbose_name='Duração',
        help_text='Duração do serviço'
    )
    tipo_duracao = models.CharField(
        max_length=10,
        choices=TIPO_DURACAO_CHOICES,
        default='minutos',
        verbose_name='Tipo de Duração'
    )
    intervalo_entre_servicos = models.PositiveIntegerField(
        default=0,
        verbose_name='Intervalo Entre Serviços (minutos)',
        help_text='Tempo de intervalo necessário após este serviço'
    )

    # Availability
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name='Status'
    )
    requer_agendamento = models.BooleanField(
        default=True,
        verbose_name='Requer Agendamento',
        help_text='Se marcado, o serviço só pode ser realizado com agendamento'
    )
    disponivel_online = models.BooleanField(
        default=True,
        verbose_name='Disponível para Agendamento Online',
        help_text='Se o serviço pode ser agendado online'
    )
    maximo_por_dia = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Máximo por Dia',
        help_text='Número máximo de vezes que o serviço pode ser realizado por dia'
    )

    # Requirements and Restrictions
    idade_minima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Idade Mínima',
        help_text='Idade mínima necessária para o serviço'
    )
    idade_maxima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Idade Máxima',
        help_text='Idade máxima permitida para o serviço'
    )
    restricoes = models.TextField(
        blank=True,
        verbose_name='Restrições',
        help_text='Restrições ou contraindicações do serviço'
    )
    preparacao_necessaria = models.TextField(
        blank=True,
        verbose_name='Preparação Necessária',
        help_text='Instruções de preparação antes do serviço'
    )
    cuidados_pos_servico = models.TextField(
        blank=True,
        verbose_name='Cuidados Pós-Serviço',
        help_text='Cuidados necessários após o serviço'
    )

    # Professional Requirements
    funcionarios_habilitados = models.ManyToManyField(
        'funcionarios.Funcionario',
        blank=True,
        related_name='servicos_habilitados',
        verbose_name='Funcionários Habilitados',
        help_text='Funcionários que podem realizar este serviço'
    )
    requer_especializacao = models.BooleanField(
        default=False,
        verbose_name='Requer Especialização',
        help_text='Se o serviço requer funcionário com especialização específica'
    )
    especializacao_necessaria = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Especialização Necessária'
    )

    # Visual
    imagem = models.ImageField(
        upload_to='servicos/imagens/',
        blank=True,
        null=True,
        verbose_name='Imagem do Serviço'
    )
    cor_identificacao = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='Cor de Identificação',
        help_text='Cor hexadecimal para identificação visual (herda da categoria se vazio)'
    )

    # SEO and Marketing
    palavras_chave = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Palavras-chave',
        help_text='Palavras-chave separadas por vírgula para busca'
    )
    destaque = models.BooleanField(
        default=False,
        verbose_name='Serviço em Destaque',
        help_text='Destacar este serviço na página principal'
    )
    ordem_exibicao = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Exibição'
    )

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['categoria__ordem', 'ordem_exibicao', 'nome']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['categoria']),
            models.Index(fields=['destaque']),
            models.Index(fields=['disponivel_online']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.categoria.nome}"

    @property
    def preco_atual(self):
        """Return current price (promotional if active, otherwise regular)"""
        if self.is_promocao_ativa and self.preco_promocional:
            return self.preco_promocional
        return self.preco

    @property
    def is_promocao_ativa(self):
        """Check if promotional price is currently active"""
        if not self.preco_promocional:
            return False
        
        from datetime import date
        today = date.today()
        
        if self.data_inicio_promocao and self.data_fim_promocao:
            return self.data_inicio_promocao <= today <= self.data_fim_promocao
        elif self.data_inicio_promocao:
            return today >= self.data_inicio_promocao
        elif self.data_fim_promocao:
            return today <= self.data_fim_promocao
        else:
            return self.status == 'promocao'

    @property
    def desconto_percentual(self):
        """Calculate discount percentage if promotional price is active"""
        if self.is_promocao_ativa and self.preco_promocional:
            return ((self.preco - self.preco_promocional) / self.preco) * 100
        return 0

    @property
    def duracao_em_minutos(self):
        """Convert duration to minutes"""
        if self.tipo_duracao == 'minutos':
            return self.duracao
        elif self.tipo_duracao == 'horas':
            return self.duracao * 60
        elif self.tipo_duracao == 'dias':
            return self.duracao * 24 * 60
        return self.duracao

    @property
    def duracao_formatada(self):
        """Return formatted duration string"""
        if self.tipo_duracao == 'minutos':
            if self.duracao < 60:
                return f"{self.duracao} min"
            else:
                horas = self.duracao // 60
                minutos = self.duracao % 60
                if minutos == 0:
                    return f"{horas}h"
                else:
                    return f"{horas}h{minutos}min"
        elif self.tipo_duracao == 'horas':
            return f"{self.duracao}h"
        elif self.tipo_duracao == 'dias':
            return f"{self.duracao} dia(s)"
        return f"{self.duracao} {self.tipo_duracao}"

    @property
    def cor_exibicao(self):
        """Return display color (own color or category color)"""
        return self.cor_identificacao or self.categoria.cor_identificacao

    @property
    def is_disponivel(self):
        """Check if service is available for booking"""
        return self.status in ['ativo', 'promocao'] and self.is_active

    def get_funcionarios_disponiveis(self):
        """Get available employees for this service"""
        if self.funcionarios_habilitados.exists():
            return self.funcionarios_habilitados.filter(
                status='ativo',
                is_active=True
            )
        else:
            # If no specific employees are set, return all active employees
            from apps.funcionarios.models import Funcionario
            return Funcionario.objects.filter(
                status='ativo',
                is_active=True
            )

    def get_total_agendamentos(self):
        """Get total number of appointments for this service"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            servico=self,
            is_active=True
        ).count()

    def get_agendamentos_concluidos(self):
        """Get total number of completed appointments"""
        from apps.agendamentos.models import Agendamento
        return Agendamento.objects.filter(
            servico=self,
            status='concluido',
            is_active=True
        ).count()

    def get_avaliacao_media(self):
        """Get average rating for this service"""
        from django.db.models import Avg
        from apps.agendamentos.models import Agendamento
        
        result = Agendamento.objects.filter(
            servico=self,
            status='concluido',
            avaliacao__isnull=False,
            is_active=True
        ).aggregate(media=Avg('avaliacao'))
        
        return result['media'] or 0

    def pode_ser_agendado_por_funcionario(self, funcionario):
        """Check if a specific employee can perform this service"""
        if not self.funcionarios_habilitados.exists():
            return True
        return self.funcionarios_habilitados.filter(id=funcionario.id).exists()

    def get_agendamentos_hoje(self):
        """Get today's appointments for this service"""
        from datetime import date
        from apps.agendamentos.models import Agendamento
        
        return Agendamento.objects.filter(
            servico=self,
            data_hora__date=date.today(),
            is_active=True
        ).exclude(status='cancelado')


class PacoteServico(BaseModel):
    """
    Model for service packages (multiple services bundled together).
    """
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Pacote'
    )
    descricao = models.TextField(
        verbose_name='Descrição do Pacote'
    )
    servicos = models.ManyToManyField(
        Servico,
        through='ItemPacote',
        related_name='pacotes',
        verbose_name='Serviços Inclusos'
    )
    preco_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço Total do Pacote'
    )
    desconto_percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Desconto (%)',
        help_text='Desconto aplicado sobre o valor individual dos serviços'
    )
    validade_dias = models.PositiveIntegerField(
        default=365,
        verbose_name='Validade (dias)',
        help_text='Número de dias para utilizar todos os serviços do pacote'
    )
    imagem = models.ImageField(
        upload_to='servicos/pacotes/',
        blank=True,
        null=True,
        verbose_name='Imagem do Pacote'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Pacote Ativo'
    )

    class Meta:
        verbose_name = 'Pacote de Serviços'
        verbose_name_plural = 'Pacotes de Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def preco_individual_total(self):
        """Calculate total price if services were bought individually"""
        total = 0
        for item in self.itens_pacote.all():
            total += item.servico.preco_atual * item.quantidade
        return total

    @property
    def valor_desconto(self):
        """Calculate discount amount"""
        individual_total = self.preco_individual_total
        return individual_total - self.preco_total

    @property
    def desconto_real_percentual(self):
        """Calculate real discount percentage"""
        individual_total = self.preco_individual_total
        if individual_total > 0:
            return ((individual_total - self.preco_total) / individual_total) * 100
        return 0

    def get_duracao_total_estimada(self):
        """Get estimated total duration for all services in the package"""
        total_minutos = 0
        for item in self.itens_pacote.all():
            total_minutos += item.servico.duracao_em_minutos * item.quantidade
        return total_minutos


class ItemPacote(models.Model):
    """
    Through model for PacoteServico and Servico relationship.
    """
    pacote = models.ForeignKey(
        PacoteServico,
        on_delete=models.CASCADE,
        related_name='itens_pacote',
        verbose_name='Pacote'
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        verbose_name='Serviço'
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantidade',
        help_text='Quantas vezes este serviço está incluído no pacote'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Execução',
        help_text='Ordem sugerida para execução dos serviços'
    )

    class Meta:
        verbose_name = 'Item do Pacote'
        verbose_name_plural = 'Itens do Pacote'
        ordering = ['ordem', 'servico__nome']
        unique_together = ['pacote', 'servico']

    def __str__(self):
        return f"{self.pacote.nome} - {self.servico.nome} ({self.quantidade}x)"