"""
Dashboard views for JT Sistemas.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import date, timedelta, datetime
import json

from apps.usuarios.models import Usuario
from apps.funcionarios.models import Funcionario
from apps.clientes.models import Cliente
from apps.agendamentos.models import Agendamento
from apps.servicos.models import Servico
from apps.core.models import AuditLog


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view with comprehensive statistics.
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic statistics
        context.update(self.get_basic_stats())
        
        # Today's appointments
        context.update(self.get_today_data())
        
        # Charts data
        context.update(self.get_charts_data())
        
        # Recent activities
        context.update(self.get_recent_activities())
        
        # Performance metrics
        context.update(self.get_performance_metrics())
        
        return context
    
    def get_basic_stats(self):
        """Get basic system statistics"""
        today = date.today()
        this_month = today.replace(day=1)
        
        return {
            'total_usuarios': Usuario.objects.filter(is_active=True).count(),
            'total_funcionarios': Funcionario.objects.filter(is_active=True, status='ativo').count(),
            'total_clientes': Cliente.objects.filter(is_active=True, status='ativo').count(),
            'total_servicos': Servico.objects.filter(is_active=True, status='ativo').count(),
            'total_agendamentos': Agendamento.objects.filter(is_active=True).count(),
            'agendamentos_mes': Agendamento.objects.filter(
                data_hora__gte=this_month,
                is_active=True
            ).count(),
            'receita_mes': Agendamento.objects.filter(
                data_hora__gte=this_month,
                status='concluido',
                pago=True,
                is_active=True
            ).aggregate(total=Sum('valor_final'))['total'] or 0,
        }
    
    def get_today_data(self):
        """Get today's data"""
        today = date.today()
        now = timezone.now()
        
        agendamentos_hoje = Agendamento.objects.filter(
            data_hora__date=today,
            is_active=True
        ).select_related('cliente', 'funcionario', 'servico')
        
        return {
            'agendamentos_hoje': agendamentos_hoje.count(),
            'agendamentos_hoje_list': agendamentos_hoje.order_by('data_hora')[:10],
            'agendamentos_concluidos_hoje': agendamentos_hoje.filter(status='concluido').count(),
            'agendamentos_cancelados_hoje': agendamentos_hoje.filter(status='cancelado').count(),
            'agendamentos_pendentes': agendamentos_hoje.filter(
                status__in=['agendado', 'confirmado'],
                data_hora__gte=now
            ).count(),
            'receita_hoje': agendamentos_hoje.filter(
                status='concluido',
                pago=True
            ).aggregate(total=Sum('valor_final'))['total'] or 0,
        }
    
    def get_charts_data(self):
        """Get data for charts and graphs"""
        # Appointments by status (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        agendamentos_status = Agendamento.objects.filter(
            data_hora__gte=thirty_days_ago,
            is_active=True
        ).values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Monthly revenue (last 12 months)
        monthly_revenue = []
        for i in range(12):
            month_start = (date.today().replace(day=1) - timedelta(days=32*i)).replace(day=1)
            next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
            
            revenue = Agendamento.objects.filter(
                data_hora__gte=month_start,
                data_hora__lt=next_month,
                status='concluido',
                pago=True,
                is_active=True
            ).aggregate(total=Sum('valor_final'))['total'] or 0
            
            monthly_revenue.append({
                'month': month_start.strftime('%b/%Y'),
                'revenue': float(revenue)
            })
        
        # Services popularity (last 30 days)
        servicos_populares = Agendamento.objects.filter(
            data_hora__gte=thirty_days_ago,
            status='concluido',
            is_active=True
        ).values('servico__nome').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Employee performance (last 30 days)
        funcionarios_performance = Agendamento.objects.filter(
            data_hora__gte=thirty_days_ago,
            status='concluido',
            is_active=True
        ).values('funcionario__nome').annotate(
            count=Count('id'),
            revenue=Sum('valor_final')
        ).order_by('-count')[:10]
        
        return {
            'agendamentos_status_data': json.dumps(list(agendamentos_status)),
            'monthly_revenue_data': json.dumps(monthly_revenue[::-1]),  # Reverse for chronological order
            'servicos_populares_data': json.dumps(list(servicos_populares)),
            'funcionarios_performance_data': json.dumps(list(funcionarios_performance)),
        }
    
    def get_recent_activities(self):
        """Get recent system activities"""
        recent_agendamentos = Agendamento.objects.filter(
            is_active=True
        ).select_related('cliente', 'funcionario', 'servico').order_by('-created_at')[:5]
        
        recent_clientes = Cliente.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5]
        
        recent_audit = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
        
        return {
            'recent_agendamentos': recent_agendamentos,
            'recent_clientes': recent_clientes,
            'recent_audit': recent_audit,
        }
    
    def get_performance_metrics(self):
        """Get performance metrics"""
        today = date.today()
        last_month = today.replace(day=1) - timedelta(days=1)
        last_month_start = last_month.replace(day=1)
        this_month_start = today.replace(day=1)
        
        # This month vs last month
        agendamentos_this_month = Agendamento.objects.filter(
            data_hora__gte=this_month_start,
            is_active=True
        ).count()
        
        agendamentos_last_month = Agendamento.objects.filter(
            data_hora__gte=last_month_start,
            data_hora__lt=this_month_start,
            is_active=True
        ).count()
        
        # Revenue comparison
        receita_this_month = Agendamento.objects.filter(
            data_hora__gte=this_month_start,
            status='concluido',
            pago=True,
            is_active=True
        ).aggregate(total=Sum('valor_final'))['total'] or 0
        
        receita_last_month = Agendamento.objects.filter(
            data_hora__gte=last_month_start,
            data_hora__lt=this_month_start,
            status='concluido',
            pago=True,
            is_active=True
        ).aggregate(total=Sum('valor_final'))['total'] or 0
        
        # Calculate growth percentages
        agendamentos_growth = 0
        if agendamentos_last_month > 0:
            agendamentos_growth = ((agendamentos_this_month - agendamentos_last_month) / agendamentos_last_month) * 100
        
        receita_growth = 0
        if receita_last_month > 0:
            receita_growth = ((receita_this_month - receita_last_month) / receita_last_month) * 100
        
        # Average rating
        avg_rating = Agendamento.objects.filter(
            status='concluido',
            avaliacao__isnull=False,
            is_active=True
        ).aggregate(avg=Avg('avaliacao'))['avg'] or 0
        
        # Cancellation rate (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        total_agendamentos = Agendamento.objects.filter(
            data_hora__gte=thirty_days_ago,
            is_active=True
        ).count()
        
        cancelados = Agendamento.objects.filter(
            data_hora__gte=thirty_days_ago,
            status='cancelado',
            is_active=True
        ).count()
        
        cancellation_rate = (cancelados / total_agendamentos * 100) if total_agendamentos > 0 else 0
        
        return {
            'agendamentos_this_month': agendamentos_this_month,
            'agendamentos_last_month': agendamentos_last_month,
            'agendamentos_growth': round(agendamentos_growth, 1),
            'receita_this_month': receita_this_month,
            'receita_last_month': receita_last_month,
            'receita_growth': round(receita_growth, 1),
            'avg_rating': round(avg_rating, 1),
            'cancellation_rate': round(cancellation_rate, 1),
        }


class CalendarView(LoginRequiredMixin, TemplateView):
    """
    Calendar view for appointments.
    """
    template_name = 'dashboard/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get appointments for calendar
        agendamentos = Agendamento.objects.filter(
            is_active=True
        ).select_related('cliente', 'funcionario', 'servico')
        
        # Format for FullCalendar
        calendar_events = []
        for agendamento in agendamentos:
            color = {
                'agendado': '#007bff',
                'confirmado': '#17a2b8',
                'em_andamento': '#ffc107',
                'concluido': '#28a745',
                'cancelado': '#dc3545',
                'nao_compareceu': '#6c757d',
                'reagendado': '#17a2b8',
            }.get(agendamento.status, '#007bff')
            
            calendar_events.append({
                'id': agendamento.id,
                'title': f"{agendamento.cliente.nome} - {agendamento.servico.nome}",
                'start': agendamento.data_hora.isoformat(),
                'end': agendamento.data_hora_fim.isoformat() if agendamento.data_hora_fim else None,
                'color': color,
                'extendedProps': {
                    'cliente': agendamento.cliente.nome,
                    'funcionario': agendamento.funcionario.nome,
                    'servico': agendamento.servico.nome,
                    'status': agendamento.get_status_display(),
                    'valor': str(agendamento.valor_final),
                    'telefone': agendamento.cliente.telefone,
                }
            })
        
        context['calendar_events'] = json.dumps(calendar_events)
        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    """
    Reports and analytics view.
    """
    template_name = 'dashboard/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Date filters from GET parameters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if not start_date:
            start_date = (date.today() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = date.today().isoformat()
        
        # Convert to datetime
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)  # Include end date
        
        # Filter appointments
        agendamentos = Agendamento.objects.filter(
            data_hora__gte=start_datetime,
            data_hora__lt=end_datetime,
            is_active=True
        )
        
        # Generate reports
        context.update({
            'start_date': start_date,
            'end_date': end_date,
            'total_agendamentos': agendamentos.count(),
            'agendamentos_concluidos': agendamentos.filter(status='concluido').count(),
            'agendamentos_cancelados': agendamentos.filter(status='cancelado').count(),
            'receita_total': agendamentos.filter(
                status='concluido', pago=True
            ).aggregate(total=Sum('valor_final'))['total'] or 0,
            'receita_pendente': agendamentos.filter(
                status='concluido', pago=False
            ).aggregate(total=Sum('valor_final'))['total'] or 0,
        })
        
        # Top services
        top_services = agendamentos.filter(
            status='concluido'
        ).values('servico__nome').annotate(
            count=Count('id'),
            revenue=Sum('valor_final')
        ).order_by('-count')[:10]
        
        # Top employees
        top_employees = agendamentos.filter(
            status='concluido'
        ).values('funcionario__nome').annotate(
            count=Count('id'),
            revenue=Sum('valor_final')
        ).order_by('-count')[:10]
        
        # Top clients
        top_clients = agendamentos.filter(
            status='concluido'
        ).values('cliente__nome').annotate(
            count=Count('id'),
            total_spent=Sum('valor_final')
        ).order_by('-total_spent')[:10]
        
        context.update({
            'top_services': top_services,
            'top_employees': top_employees,
            'top_clients': top_clients,
        })
        
        return context