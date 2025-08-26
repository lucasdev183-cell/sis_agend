"""
URL configuration for jt_sistemas project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main app URLs
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('funcionarios/', include('apps.funcionarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('agendamentos/', include('apps.agendamentos.urls')),
    path('servicos/', include('apps.servicos.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('configuracoes/', include('apps.configuracoes.urls')),
    
    # API URLs
    path('api/', include('apps.core.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "JT Sistemas - Administração"
admin.site.site_title = "JT Sistemas Admin"
admin.site.index_title = "Painel Administrativo"