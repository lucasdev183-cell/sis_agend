"""
Forms for usuarios app.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div, Field
from crispy_forms.bootstrap import PrependedText, AppendedText

from .models import Usuario, PerfilUsuario


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with enhanced styling.
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Nome de usuário',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Senha'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='mb-3'),
                Field('password', css_class='mb-3'),
                Div(
                    Field('remember_me', css_class='form-check-input me-2'),
                    HTML('<label class="form-check-label" for="id_remember_me">Lembrar de mim</label>'),
                    css_class='form-check mb-3'
                ),
                Submit('submit', 'Entrar', css_class='btn btn-primary btn-lg w-100 mb-3'),
                css_class='login-form'
            )
        )


class UsuarioCreateForm(UserCreationForm):
    """
    Form for creating new users.
    """
    nome = forms.CharField(
        max_length=100,
        label='Nome Completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+55 11 99999-9999'
        })
    )
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_CHOICES,
        label='Tipo de Usuário',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Permission fields
    pode_cadastrar_cliente = forms.BooleanField(
        required=False,
        label='Pode Cadastrar Clientes',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_cadastrar_funcionario = forms.BooleanField(
        required=False,
        label='Pode Cadastrar Funcionários',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_cadastrar_cargo = forms.BooleanField(
        required=False,
        label='Pode Cadastrar Cargos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_agendar = forms.BooleanField(
        required=False,
        initial=True,
        label='Pode Agendar Serviços',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_ver_agendamentos = forms.BooleanField(
        required=False,
        initial=True,
        label='Pode Ver Agendamentos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_editar_agendamentos = forms.BooleanField(
        required=False,
        label='Pode Editar Agendamentos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_cancelar_agendamentos = forms.BooleanField(
        required=False,
        label='Pode Cancelar Agendamentos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_ver_relatorios = forms.BooleanField(
        required=False,
        label='Pode Ver Relatórios',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pode_gerenciar_configuracoes = forms.BooleanField(
        required=False,
        label='Pode Gerenciar Configurações',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'nome', 'email', 'telefone', 'tipo_usuario',
            'password1', 'password2',
            'pode_cadastrar_cliente', 'pode_cadastrar_funcionario', 'pode_cadastrar_cargo',
            'pode_agendar', 'pode_ver_agendamentos', 'pode_editar_agendamentos',
            'pode_cancelar_agendamentos', 'pode_ver_relatorios', 'pode_gerenciar_configuracoes'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            Div(
                HTML('<h4 class="mb-3">Informações Básicas</h4>'),
                Row(
                    Column('nome', css_class='col-md-6'),
                    Column('username', css_class='col-md-6'),
                ),
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('telefone', css_class='col-md-6'),
                ),
                Row(
                    Column('tipo_usuario', css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Senha</h4>'),
                Row(
                    Column('password1', css_class='col-md-6'),
                    Column('password2', css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Permissões</h4>'),
                Row(
                    Column(
                        Field('pode_cadastrar_cliente'),
                        Field('pode_cadastrar_funcionario'),
                        Field('pode_cadastrar_cargo'),
                        css_class='col-md-4'
                    ),
                    Column(
                        Field('pode_agendar'),
                        Field('pode_ver_agendamentos'),
                        Field('pode_editar_agendamentos'),
                        css_class='col-md-4'
                    ),
                    Column(
                        Field('pode_cancelar_agendamentos'),
                        Field('pode_ver_relatorios'),
                        Field('pode_gerenciar_configuracoes'),
                        css_class='col-md-4'
                    ),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                Submit('submit', 'Criar Usuário', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "usuarios:list" %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='d-flex justify-content-end'
            )
        )


class UsuarioUpdateForm(forms.ModelForm):
    """
    Form for updating existing users.
    """
    nome = forms.CharField(
        max_length=100,
        label='Nome Completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+55 11 99999-9999'
        })
    )
    
    class Meta:
        model = Usuario
        fields = [
            'nome', 'email', 'telefone', 'tipo_usuario', 'avatar',
            'pode_cadastrar_cliente', 'pode_cadastrar_funcionario', 'pode_cadastrar_cargo',
            'pode_agendar', 'pode_ver_agendamentos', 'pode_editar_agendamentos',
            'pode_cancelar_agendamentos', 'pode_ver_relatorios', 'pode_gerenciar_configuracoes',
            'is_active'
        ]
        widgets = {
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_cadastrar_cliente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_cadastrar_funcionario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_cadastrar_cargo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_agendar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_ver_agendamentos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_editar_agendamentos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_cancelar_agendamentos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_ver_relatorios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pode_gerenciar_configuracoes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': '', 'enctype': 'multipart/form-data'}
        
        self.helper.layout = Layout(
            Div(
                HTML('<h4 class="mb-3">Informações Básicas</h4>'),
                Row(
                    Column('nome', css_class='col-md-6'),
                    Column('email', css_class='col-md-6'),
                ),
                Row(
                    Column('telefone', css_class='col-md-6'),
                    Column('tipo_usuario', css_class='col-md-6'),
                ),
                Row(
                    Column('avatar', css_class='col-md-6'),
                    Column(Field('is_active'), css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Permissões</h4>'),
                Row(
                    Column(
                        Field('pode_cadastrar_cliente'),
                        Field('pode_cadastrar_funcionario'),
                        Field('pode_cadastrar_cargo'),
                        css_class='col-md-4'
                    ),
                    Column(
                        Field('pode_agendar'),
                        Field('pode_ver_agendamentos'),
                        Field('pode_editar_agendamentos'),
                        css_class='col-md-4'
                    ),
                    Column(
                        Field('pode_cancelar_agendamentos'),
                        Field('pode_ver_relatorios'),
                        Field('pode_gerenciar_configuracoes'),
                        css_class='col-md-4'
                    ),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                Submit('submit', 'Atualizar Usuário', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "usuarios:detail" object.pk %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='d-flex justify-content-end'
            )
        )


class PerfilUsuarioForm(forms.ModelForm):
    """
    Form for user profile information.
    """
    class Meta:
        model = PerfilUsuario
        fields = [
            'data_nascimento', 'cpf', 'endereco', 'cidade', 'estado', 'cep',
            'cargo', 'departamento', 'data_admissao',
            'tema_preferido', 'idioma', 'receber_notificacoes_email', 'receber_notificacoes_whatsapp'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',
                'placeholder': 'SP'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000'
            }),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'data_admissao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tema_preferido': forms.Select(attrs={'class': 'form-select'}),
            'idioma': forms.Select(attrs={'class': 'form-select'}),
            'receber_notificacoes_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'receber_notificacoes_whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            Div(
                HTML('<h4 class="mb-3">Informações Pessoais</h4>'),
                Row(
                    Column('data_nascimento', css_class='col-md-6'),
                    Column('cpf', css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Endereço</h4>'),
                Row(
                    Column('endereco', css_class='col-md-8'),
                    Column('cidade', css_class='col-md-4'),
                ),
                Row(
                    Column('estado', css_class='col-md-6'),
                    Column('cep', css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Informações Profissionais</h4>'),
                Row(
                    Column('cargo', css_class='col-md-6'),
                    Column('departamento', css_class='col-md-6'),
                ),
                Row(
                    Column('data_admissao', css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                HTML('<h4 class="mb-3">Preferências</h4>'),
                Row(
                    Column('tema_preferido', css_class='col-md-6'),
                    Column('idioma', css_class='col-md-6'),
                ),
                Row(
                    Column(Field('receber_notificacoes_email'), css_class='col-md-6'),
                    Column(Field('receber_notificacoes_whatsapp'), css_class='col-md-6'),
                ),
                css_class='card-body mb-4'
            ),
            Div(
                Submit('submit', 'Atualizar Perfil', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "dashboard:home" %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='d-flex justify-content-end'
            )
        )