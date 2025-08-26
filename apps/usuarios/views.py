"""
User views for JT Sistemas.
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

from .models import Usuario, PerfilUsuario
from .forms import CustomLoginForm, UsuarioCreateForm, UsuarioUpdateForm, PerfilUsuarioForm


class CustomLoginView(LoginView):
    """
    Custom login view with enhanced features.
    """
    template_name = 'usuarios/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Handle successful login"""
        user = form.get_user()
        
        # Check if account is locked
        if user.is_account_locked:
            messages.error(
                self.request, 
                'Sua conta está temporariamente bloqueada devido a múltiplas tentativas de login falhadas. '
                'Tente novamente em alguns minutos.'
            )
            return self.form_invalid(form)
        
        # Reset failed attempts on successful login
        user.reset_failed_login_attempts()
        
        # Save login IP
        user.ultimo_login_ip = self.get_client_ip()
        user.save(update_fields=['ultimo_login_ip'])
        
        # Log successful login
        from apps.core.models import AuditLog
        AuditLog.objects.create(
            user=user,
            action='login',
            model_name='Usuario',
            object_id=user.id,
            object_repr=str(user),
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(self.request, f'Bem-vindo, {user.nome_display}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle failed login"""
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = Usuario.objects.get(username=username)
                user.increment_failed_login_attempts()
            except Usuario.DoesNotExist:
                pass
        
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class CustomLogoutView(LogoutView):
    """
    Custom logout view.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Log logout
            from apps.core.models import AuditLog
            AuditLog.objects.create(
                user=request.user,
                action='logout',
                model_name='Usuario',
                object_id=request.user.id,
                object_repr=str(request.user),
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.info(request, 'Você foi desconectado com sucesso.')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class UsuarioCreateView(LoginRequiredMixin, CreateView):
    """
    Create new user view.
    """
    model = Usuario
    form_class = UsuarioCreateForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:list')
    
    def dispatch(self, request, *args, **kwargs):
        # Check permissions
        if not request.user.has_permission('pode_cadastrar_funcionario'):
            messages.error(request, 'Você não tem permissão para criar usuários.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        
        # Log user creation
        from apps.core.models import AuditLog
        response = super().form_valid(form)
        
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            model_name='Usuario',
            object_id=self.object.id,
            object_repr=str(self.object),
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        return response
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class UsuarioListView(LoginRequiredMixin, ListView):
    """
    List all users view.
    """
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Usuario.objects.filter(is_active=True).select_related('perfil')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by type
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_usuario=tipo)
        
        return queryset.order_by('nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        return context


class UsuarioDetailView(LoginRequiredMixin, DetailView):
    """
    User detail view.
    """
    model = Usuario
    template_name = 'usuarios/usuario_detail.html'
    context_object_name = 'usuario'
    
    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).select_related('perfil')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's recent activities
        from apps.core.models import AuditLog
        context['recent_activities'] = AuditLog.objects.filter(
            user=self.object
        ).order_by('-timestamp')[:10]
        
        # Get user's permissions
        context['permissions'] = self.object.get_permissions_list()
        
        return context


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update user view.
    """
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'usuarios/usuario_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Users can edit their own profile or admins can edit any profile
        user_to_edit = self.get_object()
        if request.user != user_to_edit and not request.user.has_permission('pode_cadastrar_funcionario'):
            messages.error(request, 'Você não tem permissão para editar este usuário.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('usuarios:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        
        # Log user update
        from apps.core.models import AuditLog
        response = super().form_valid(form)
        
        AuditLog.objects.create(
            user=self.request.user,
            action='update',
            model_name='Usuario',
            object_id=self.object.id,
            object_repr=str(self.object),
            changes=form.changed_data,
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        return response
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class PerfilView(LoginRequiredMixin, UpdateView):
    """
    User profile view and edit.
    """
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil.html'
    success_url = reverse_lazy('usuarios:perfil')
    
    def get_object(self, queryset=None):
        """Get or create user profile"""
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=self.request.user
        )
        return perfil
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        
        # Get user's recent activities
        from apps.core.models import AuditLog
        context['recent_activities'] = AuditLog.objects.filter(
            user=self.request.user
        ).order_by('-timestamp')[:5]
        
        return context


class AlterarSenhaView(LoginRequiredMixin, UpdateView):
    """
    Change password view.
    """
    model = Usuario
    fields = []  # We'll handle password change differently
    template_name = 'usuarios/alterar_senha.html'
    success_url = reverse_lazy('usuarios:perfil')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate current password
        if not user.check_password(current_password):
            messages.error(request, 'Senha atual incorreta.')
            return self.get(request, *args, **kwargs)
        
        # Validate new password
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return self.get(request, *args, **kwargs)
        
        if len(new_password) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
            return self.get(request, *args, **kwargs)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Log password change
        from apps.core.models import AuditLog
        AuditLog.objects.create(
            user=user,
            action='update',
            model_name='Usuario',
            object_id=user.id,
            object_repr=str(user),
            changes=['password'],
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, 'Senha alterada com sucesso!')
        return redirect(self.success_url)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip