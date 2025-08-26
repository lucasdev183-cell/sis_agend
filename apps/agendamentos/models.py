"""
Appointment models for JT Sistemas.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import BaseModel


class Agendamento(BaseModel):
    """
    Model for appointments/bookings.
    """
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('nao_compareceu', 'Não Compareceu'),
        ('reagendado', 'Reagendado'),
    ]

    ORIGEM_CHOICES = [
        ('presencial', 'Presencial'),
        ('telefone', 'Telefone'),
        ('whatsapp', 'WhatsApp'),
        ('online', 'Site/App'),
        ('indicacao', 'Indicação'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência'),
        ('boleto', 'Boleto'),
        ('nao_definido', 'Não Definido'),
    ]

    # Basic Information
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='agendamentos',
        verbose_name='Cliente'
    )
    funcionario = models.ForeignKey(
        'funcionarios.Funcionario',
        on_delete=models.PROTECT,
        related_name='agendamentos',
        verbose_name='Funcionário'
    )
    servico = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.PROTECT,
        related_name='agendamentos',
        verbose_name='Serviço'
    )
    pacote = models.ForeignKey(
        'servicos.PacoteServico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos',
        verbose_name='Pacote de Serviços',
        help_text='Se este agendamento faz parte de um pacote'
    )

    # Scheduling Information
    data_hora = models.DateTimeField(
        verbose_name='Data e Hora do Agendamento'
    )
    data_hora_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data e Hora de Término',
        help_text='Calculado automaticamente baseado na duração do serviço'
    )
    duracao_prevista = models.PositiveIntegerField(
        verbose_name='Duração Prevista (minutos)',
        help_text='Duração prevista em minutos (copiada do serviço)'
    )
    duracao_real = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Duração Real (minutos)',
        help_text='Duração real do atendimento'
    )

    # Status and Control
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='agendado',
        verbose_name='Status'
    )
    data_confirmacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Confirmação'
    )
    data_inicio_atendimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Início do Atendimento'
    )
    data_fim_atendimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Fim do Atendimento'
    )
    data_cancelamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Cancelamento'
    )

    # Origin and Source
    origem = models.CharField(
        max_length=20,
        choices=ORIGEM_CHOICES,
        default='presencial',
        verbose_name='Origem do Agendamento'
    )
    usuario_agendou = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos_criados',
        verbose_name='Usuário que Agendou'
    )
    usuario_confirmou = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos_confirmados',
        verbose_name='Usuário que Confirmou'
    )
    usuario_cancelou = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos_cancelados',
        verbose_name='Usuário que Cancelou'
    )

    # Financial Information
    valor_servico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Serviço',
        help_text='Valor cobrado pelo serviço (copiado do serviço no momento do agendamento)'
    )
    desconto_aplicado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Desconto Aplicado'
    )
    valor_final = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Final',
        help_text='Valor final após aplicação de descontos'
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='nao_definido',
        verbose_name='Forma de Pagamento'
    )
    pago = models.BooleanField(
        default=False,
        verbose_name='Pagamento Realizado'
    )
    data_pagamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Pagamento'
    )

    # Additional Information
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações gerais sobre o agendamento'
    )
    observacoes_cliente = models.TextField(
        blank=True,
        verbose_name='Observações do Cliente',
        help_text='Observações ou solicitações específicas do cliente'
    )
    observacoes_funcionario = models.TextField(
        blank=True,
        verbose_name='Observações do Funcionário',
        help_text='Observações do funcionário sobre o atendimento'
    )
    motivo_cancelamento = models.TextField(
        blank=True,
        verbose_name='Motivo do Cancelamento'
    )

    # Evaluation and Feedback
    avaliacao = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Avaliação (1-5)',
        help_text='Avaliação do cliente sobre o serviço'
    )
    comentario_avaliacao = models.TextField(
        blank=True,
        verbose_name='Comentário da Avaliação'
    )
    data_avaliacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da Avaliação'
    )

    # Notifications and Communication
    lembrete_enviado = models.BooleanField(
        default=False,
        verbose_name='Lembrete Enviado',
        help_text='Se o lembrete foi enviado ao cliente'
    )
    data_lembrete = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Lembrete'
    )
    confirmacao_enviada = models.BooleanField(
        default=False,
        verbose_name='Confirmação Enviada',
        help_text='Se a confirmação foi enviada ao cliente'
    )

    # Rescheduling
    agendamento_original = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reagendamentos',
        verbose_name='Agendamento Original',
        help_text='Referência ao agendamento original em caso de reagendamento'
    )
    numero_reagendamentos = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Reagendamentos'
    )

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['data_hora']),
            models.Index(fields=['status']),
            models.Index(fields=['cliente']),
            models.Index(fields=['funcionario']),
            models.Index(fields=['servico']),
            models.Index(fields=['data_hora', 'status']),
        ]

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def save(self, *args, **kwargs):
        # Calculate end time based on service duration
        if not self.data_hora_fim and self.data_hora and self.duracao_prevista:
            from datetime import timedelta
            self.data_hora_fim = self.data_hora + timedelta(minutes=self.duracao_prevista)
        
        # Set service values if not set
        if not self.valor_servico:
            self.valor_servico = self.servico.preco_atual
        
        if not self.duracao_prevista:
            self.duracao_prevista = self.servico.duracao_em_minutos
        
        # Calculate final value
        self.valor_final = self.valor_servico - self.desconto_aplicado
        
        # Set confirmation date when status changes to confirmed
        if self.status == 'confirmado' and not self.data_confirmacao:
            self.data_confirmacao = timezone.now()
        
        # Set cancellation date when status changes to cancelled
        if self.status == 'cancelado' and not self.data_cancelamento:
            self.data_cancelamento = timezone.now()
        
        # Set start time when status changes to in progress
        if self.status == 'em_andamento' and not self.data_inicio_atendimento:
            self.data_inicio_atendimento = timezone.now()
        
        # Set end time and calculate real duration when completed
        if self.status == 'concluido' and not self.data_fim_atendimento:
            self.data_fim_atendimento = timezone.now()
            if self.data_inicio_atendimento:
                delta = self.data_fim_atendimento - self.data_inicio_atendimento
                self.duracao_real = int(delta.total_seconds() / 60)
        
        super().save(*args, **kwargs)

    @property
    def is_hoje(self):
        """Check if appointment is today"""
        from datetime import date
        return self.data_hora.date() == date.today()

    @property
    def is_passado(self):
        """Check if appointment is in the past"""
        return self.data_hora < timezone.now()

    @property
    def is_futuro(self):
        """Check if appointment is in the future"""
        return self.data_hora > timezone.now()

    @property
    def pode_ser_cancelado(self):
        """Check if appointment can be cancelled"""
        return self.status in ['agendado', 'confirmado'] and not self.is_passado

    @property
    def pode_ser_confirmado(self):
        """Check if appointment can be confirmed"""
        return self.status == 'agendado' and not self.is_passado

    @property
    def pode_iniciar_atendimento(self):
        """Check if service can be started"""
        return self.status in ['agendado', 'confirmado'] and self.is_hoje

    @property
    def pode_ser_concluido(self):
        """Check if appointment can be completed"""
        return self.status == 'em_andamento'

    @property
    def tempo_ate_agendamento(self):
        """Calculate time until appointment"""
        if self.is_futuro:
            delta = self.data_hora - timezone.now()
            return delta
        return None

    @property
    def tempo_desde_agendamento(self):
        """Calculate time since appointment was scheduled"""
        delta = timezone.now() - self.created_at
        return delta

    @property
    def status_cor(self):
        """Return color class for status"""
        cores = {
            'agendado': 'primary',
            'confirmado': 'info',
            'em_andamento': 'warning',
            'concluido': 'success',
            'cancelado': 'danger',
            'nao_compareceu': 'secondary',
            'reagendado': 'info',
        }
        return cores.get(self.status, 'secondary')

    @property
    def percentual_desconto(self):
        """Calculate discount percentage"""
        if self.valor_servico > 0:
            return (self.desconto_aplicado / self.valor_servico) * 100
        return 0

    def confirmar(self, usuario=None):
        """Confirm the appointment"""
        if self.pode_ser_confirmado:
            self.status = 'confirmado'
            self.data_confirmacao = timezone.now()
            if usuario:
                self.usuario_confirmou = usuario
            self.save()
            return True
        return False

    def cancelar(self, motivo='', usuario=None):
        """Cancel the appointment"""
        if self.pode_ser_cancelado:
            self.status = 'cancelado'
            self.data_cancelamento = timezone.now()
            self.motivo_cancelamento = motivo
            if usuario:
                self.usuario_cancelou = usuario
            self.save()
            return True
        return False

    def iniciar_atendimento(self):
        """Start the service"""
        if self.pode_iniciar_atendimento:
            self.status = 'em_andamento'
            self.data_inicio_atendimento = timezone.now()
            self.save()
            return True
        return False

    def concluir_atendimento(self, observacoes_funcionario=''):
        """Complete the service"""
        if self.pode_ser_concluido:
            self.status = 'concluido'
            self.data_fim_atendimento = timezone.now()
            if observacoes_funcionario:
                self.observacoes_funcionario = observacoes_funcionario
            
            # Calculate real duration
            if self.data_inicio_atendimento:
                delta = self.data_fim_atendimento - self.data_inicio_atendimento
                self.duracao_real = int(delta.total_seconds() / 60)
            
            # Update client's last service date
            self.cliente.atualizar_ultimo_atendimento()
            
            self.save()
            return True
        return False

    def reagendar(self, nova_data_hora, motivo='', usuario=None):
        """Reschedule the appointment"""
        if self.pode_ser_cancelado:
            # Create new appointment
            novo_agendamento = Agendamento.objects.create(
                cliente=self.cliente,
                funcionario=self.funcionario,
                servico=self.servico,
                pacote=self.pacote,
                data_hora=nova_data_hora,
                duracao_prevista=self.duracao_prevista,
                valor_servico=self.valor_servico,
                desconto_aplicado=self.desconto_aplicado,
                forma_pagamento=self.forma_pagamento,
                origem=self.origem,
                observacoes=self.observacoes,
                observacoes_cliente=self.observacoes_cliente,
                agendamento_original=self.agendamento_original or self,
                numero_reagendamentos=self.numero_reagendamentos + 1,
                usuario_agendou=usuario
            )
            
            # Mark current appointment as rescheduled
            self.status = 'reagendado'
            self.motivo_cancelamento = f"Reagendado: {motivo}"
            if usuario:
                self.usuario_cancelou = usuario
            self.save()
            
            return novo_agendamento
        return None

    def avaliar(self, nota, comentario=''):
        """Rate the service"""
        if self.status == 'concluido':
            self.avaliacao = nota
            self.comentario_avaliacao = comentario
            self.data_avaliacao = timezone.now()
            self.save()
            return True
        return False

    def marcar_pagamento(self, forma_pagamento=None):
        """Mark as paid"""
        self.pago = True
        self.data_pagamento = timezone.now()
        if forma_pagamento:
            self.forma_pagamento = forma_pagamento
        self.save()

    def get_historico_status(self):
        """Get status change history (would need a separate model for full implementation)"""
        # This is a simplified version - in a real app, you'd want a separate StatusHistory model
        historico = []
        if self.created_at:
            historico.append({'status': 'agendado', 'data': self.created_at})
        if self.data_confirmacao:
            historico.append({'status': 'confirmado', 'data': self.data_confirmacao})
        if self.data_inicio_atendimento:
            historico.append({'status': 'em_andamento', 'data': self.data_inicio_atendimento})
        if self.data_fim_atendimento:
            historico.append({'status': 'concluido', 'data': self.data_fim_atendimento})
        if self.data_cancelamento:
            historico.append({'status': 'cancelado', 'data': self.data_cancelamento})
        return historico


class StatusAgendamento(BaseModel):
    """
    Model to track status changes in appointments (audit trail).
    """
    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE,
        related_name='historico_status',
        verbose_name='Agendamento'
    )
    status_anterior = models.CharField(
        max_length=20,
        choices=Agendamento.STATUS_CHOICES,
        blank=True,
        verbose_name='Status Anterior'
    )
    status_novo = models.CharField(
        max_length=20,
        choices=Agendamento.STATUS_CHOICES,
        verbose_name='Status Novo'
    )
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário Responsável'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações sobre a Mudança'
    )
    data_mudanca = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Mudança'
    )

    class Meta:
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        ordering = ['-data_mudanca']

    def __str__(self):
        return f"{self.agendamento} - {self.status_anterior} → {self.status_novo}"


class Notificacao(BaseModel):
    """
    Model for notifications sent to clients.
    """
    TIPO_CHOICES = [
        ('lembrete', 'Lembrete'),
        ('confirmacao', 'Confirmação'),
        ('cancelamento', 'Cancelamento'),
        ('reagendamento', 'Reagendamento'),
        ('avaliacao', 'Solicitação de Avaliação'),
        ('promocao', 'Promoção'),
    ]

    CANAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push Notification'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviada', 'Enviada'),
        ('entregue', 'Entregue'),
        ('lida', 'Lida'),
        ('erro', 'Erro'),
    ]

    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name='Agendamento'
    )
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name='Cliente'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Notificação'
    )
    canal = models.CharField(
        max_length=20,
        choices=CANAL_CHOICES,
        verbose_name='Canal de Envio'
    )
    destinatario = models.CharField(
        max_length=100,
        verbose_name='Destinatário',
        help_text='Número de telefone, email, etc.'
    )
    assunto = models.CharField(
        max_length=200,
        verbose_name='Assunto'
    )
    mensagem = models.TextField(
        verbose_name='Mensagem'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    data_agendamento = models.DateTimeField(
        verbose_name='Data de Agendamento do Envio'
    )
    data_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Envio'
    )
    data_entrega = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Entrega'
    )
    data_leitura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Leitura'
    )
    erro_detalhes = models.TextField(
        blank=True,
        verbose_name='Detalhes do Erro'
    )
    tentativas = models.PositiveIntegerField(
        default=0,
        verbose_name='Tentativas de Envio'
    )

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_agendamento']

    def __str__(self):
        return f"{self.cliente.nome} - {self.get_tipo_display()} - {self.get_canal_display()}"

    def marcar_como_enviada(self):
        """Mark notification as sent"""
        self.status = 'enviada'
        self.data_envio = timezone.now()
        self.save()

    def marcar_como_entregue(self):
        """Mark notification as delivered"""
        self.status = 'entregue'
        self.data_entrega = timezone.now()
        self.save()

    def marcar_como_lida(self):
        """Mark notification as read"""
        self.status = 'lida'
        self.data_leitura = timezone.now()
        self.save()

    def marcar_erro(self, detalhes_erro):
        """Mark notification as failed"""
        self.status = 'erro'
        self.erro_detalhes = detalhes_erro
        self.tentativas += 1
        self.save()