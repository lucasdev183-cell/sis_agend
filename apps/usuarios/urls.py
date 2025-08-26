"""
URLs for usuarios app.
"""
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # User management
    path('', views.UsuarioListView.as_view(), name='list'),
    path('create/', views.UsuarioCreateView.as_view(), name='create'),
    path('<int:pk>/', views.UsuarioDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.UsuarioUpdateView.as_view(), name='edit'),
    
    # Profile management
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('alterar-senha/', views.AlterarSenhaView.as_view(), name='alterar_senha'),
]