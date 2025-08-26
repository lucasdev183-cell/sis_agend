# JT Sistemas - Sistema de Gestão Empresarial

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Visão Geral

O **JT Sistemas** é uma plataforma completa de gestão empresarial desenvolvida em Django, projetada para oferecer uma experiência moderna e intuitiva no gerenciamento de negócios. O sistema combina funcionalidades robustas com uma interface elegante e responsiva, proporcionando controle total sobre usuários, funcionários, clientes, serviços e agendamentos.

### ✨ Proposta do Sistema

O JT Sistemas foi concebido para ser a solução definitiva para empresas que buscam:

- **Gestão Centralizada**: Controle total de usuários, funcionários e clientes em uma única plataforma
- **Sistema de Agendamentos**: Funcionalidade completa para agendamento de serviços com controle de status
- **Relatórios Inteligentes**: Dashboard com métricas e relatórios detalhados para tomada de decisões
- **Integração WhatsApp**: Bot automatizado para atendimento e agendamentos via WhatsApp
- **Interface Moderna**: Design profissional com animações fluidas e experiência de usuário premium
- **Segurança Avançada**: Sistema de permissões granulares e auditoria completa

## 🎨 Sistema de Design e Paleta de Cores

### Paleta de Cores Principal

```css
/* Cores Primárias */
--primary-color: #2563eb        /* Azul Primário - Elementos principais */
--primary-dark: #1d4ed8         /* Azul Escuro - Estados hover/active */
--primary-light: #3b82f6        /* Azul Claro - Elementos secundários */

/* Cores Funcionais */
--success-color: #059669        /* Verde - Sucesso/Confirmações */
--success-light: #10b981        /* Verde Claro - Estados de sucesso */
--danger-color: #dc2626         /* Vermelho - Erros/Exclusões */
--danger-light: #ef4444         /* Vermelho Claro - Estados de alerta */
--warning-color: #d97706        /* Laranja - Avisos */
--info-color: #0891b2          /* Azul Info - Informações */

/* Tons Neutros */
--gray-50: #f8fafc             /* Fundo claro */
--gray-100: #f1f5f9            /* Fundo secundário */
--gray-200: #e2e8f0            /* Bordas sutis */
--gray-300: #cbd5e1            /* Bordas padrão */
--gray-400: #94a3b8            /* Texto secundário */
--gray-500: #64748b            /* Texto padrão */
--gray-600: #475569            /* Texto escuro */
--gray-700: #334155            /* Texto principal */
--gray-800: #1e293b            /* Texto destaque */
--gray-900: #0f172a            /* Texto máximo contraste */
```

### Gradientes e Efeitos

- **Fundo Principal**: Gradiente diagonal do cinza-50 ao cinza-100
- **Login**: Gradiente diagonal do roxo ao azul (#667eea → #764ba2)
- **Sidebar**: Gradiente vertical do azul escuro (#2c3e50 → #34495e)
- **Cards**: Sombras suaves com elevação progressiva no hover

## 🎯 Barra Lateral Interativa

### Características Principais

A barra lateral é o coração da navegação do sistema, oferecendo uma experiência fluida e intuitiva:

#### 📐 Dimensões e Layout
- **Largura Colapsada**: 70px (modo compacto)
- **Largura Expandida**: 280px (modo completo)
- **Altura**: 100vh (tela completa)
- **Posição**: Fixa à esquerda

#### 🎭 Estados e Comportamentos

1. **Estado Colapsado (Padrão)**
   - Mostra apenas ícones
   - Textos ocultos com `opacity: 0`
   - Largura de 70px

2. **Estado Expandido (Hover/Click)**
   - Exibe textos e ícones completos
   - Transição suave de 0.3s
   - Largura de 280px

3. **Estado Mobile**
   - Overlay completo na tela
   - Fundo semitransparente
   - Slide-in animation

## 🏗️ Funcionalidades do Sistema

### 👤 Gestão de Usuários

#### Tipos de Usuário
- **Master**: Acesso completo ao sistema
- **Restrito**: Permissões personalizáveis

#### Permissões Granulares
- Cadastrar clientes
- Cadastrar funcionários  
- Cadastrar cargos
- Agendar serviços
- Visualizar agendamentos
- Acessar relatórios

#### Funcionalidades
- ✅ Cadastro com validação completa
- ✅ Sistema de autenticação seguro
- ✅ Edição de perfis
- ✅ Controle de permissões
- ✅ Auditoria de ações

### 👥 Gestão de Funcionários

- **Cadastro Completo**: Nome, cargo, contato, informações pessoais
- **Vinculação com Usuários**: Funcionários podem ter acesso ao sistema
- **Controle de Cargos**: Hierarquia organizacional
- **Status de Atividade**: Ativar/desativar funcionários

### 👨‍💼 Gestão de Clientes

- **Cadastro Simplificado**: Dados essenciais para atendimento
- **Histórico de Agendamentos**: Visualização completa do relacionamento
- **Informações de Contato**: Telefone, email, endereço
- **Status de Cliente**: Controle de clientes ativos

### 📅 Sistema de Agendamentos

#### Funcionalidades Principais
- **Agendamento Completo**: Data, hora, cliente, funcionário, serviço
- **Controle de Status**: Agendado, em andamento, concluído, cancelado
- **Visualização Calendário**: Interface intuitiva para gestão
- **Histórico Completo**: Rastreamento de todos os agendamentos

#### Status de Agendamento
1. **Agendado** - Novo agendamento criado
2. **Em Andamento** - Serviço sendo executado
3. **Concluído** - Serviço finalizado
4. **Cancelado** - Agendamento cancelado

### 📊 Dashboard e Relatórios

#### Métricas Principais
- Total de usuários no sistema
- Quantidade de funcionários ativos
- Total de agendamentos
- Agendamentos do dia
- Receita mensal

#### Relatórios Disponíveis
- **Agendamentos por Período**: Filtros customizáveis
- **Performance de Funcionários**: Produtividade individual
- **Análise de Clientes**: Frequência e relacionamento
- **Relatórios Financeiros**: Controle de receitas

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- Redis (opcional, para cache)

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/jt-sistemas.git
cd jt-sistemas
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
# PGHOST=localhost
# PGPORT=5432
# PGUSER=postgres
# PGPASSWORD=sua_senha
# PGDATABASE=jt_sistemas
```

5. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Colete os arquivos estáticos**
```bash
python manage.py collectstatic
```

8. **Execute o servidor**
```bash
python manage.py runserver
```

## 🗄️ Configuração do Banco de Dados

O sistema utiliza um arquivo `database.py` personalizado para gerenciar conexões PostgreSQL:

```python
# Configurações no .env
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=sua_senha
PGDATABASE=jt_sistemas
```

O arquivo `database.py` fornece funções utilitárias:
- `get_connection()`: Cria conexão com o banco
- `test_connection()`: Testa a conexão
- `execute_query()`: Executa consultas SQL

## 📁 Estrutura do Projeto

```
jt_sistemas/
├── jt_sistemas/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/           # Modelos base e utilitários
│   ├── usuarios/       # Gestão de usuários
│   ├── funcionarios/   # Gestão de funcionários
│   ├── clientes/       # Gestão de clientes
│   ├── agendamentos/   # Sistema de agendamentos
│   ├── servicos/       # Gestão de serviços
│   ├── relatorios/     # Relatórios e analytics
│   ├── configuracoes/  # Configurações do sistema
│   └── dashboard/      # Dashboard principal
├── templates/          # Templates HTML
├── static/            # Arquivos estáticos
├── media/             # Uploads de usuário
├── database.py        # Configuração personalizada do BD
├── requirements.txt   # Dependências Python
└── manage.py
```

## 🎨 Frontend e Design

### Tecnologias Utilizadas
- **Bootstrap 5.3**: Framework CSS responsivo
- **Font Awesome 6.4.0**: Ícones
- **Inter Font**: Tipografia moderna
- **Chart.js**: Gráficos e visualizações
- **Vanilla JavaScript**: Interatividade sem dependências pesadas

### Componentes Principais
- Sidebar interativa com animações
- Cards com hover effects
- Formulários com validação
- Modais responsivos
- Gráficos interativos

## 🔒 Segurança

### Recursos de Segurança
- Autenticação robusta com Django Auth
- Permissões granulares por usuário
- Auditoria completa de ações
- Proteção CSRF
- Validação de dados server-side e client-side
- Controle de tentativas de login
- Bloqueio automático de contas

### Configurações de Produção
- HTTPS obrigatório
- Headers de segurança
- Configurações de sessão seguras
- Proteção contra ataques comuns

## 📊 API e Integrações

### Django REST Framework
- API RESTful completa
- Serializers para todos os modelos
- Autenticação por token
- Paginação automática

### Integração WhatsApp
- Bot automatizado para atendimento
- Agendamentos via WhatsApp
- Notificações automáticas
- Configuração via Meta Business API

## 🧪 Testes

### Estrutura de Testes
```bash
# Executar todos os testes
python manage.py test

# Executar testes específicos
python manage.py test apps.usuarios

# Com coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deploy

### Configurações de Produção

1. **Variáveis de Ambiente**
```bash
DEBUG=False
SECRET_KEY=sua-chave-secreta-segura
ALLOWED_HOSTS=seu-dominio.com
SECURE_SSL_REDIRECT=True
```

2. **Servidor Web**
```bash
# Com Gunicorn
gunicorn jt_sistemas.wsgi:application

# Com Nginx (configuração de exemplo)
# /etc/nginx/sites-available/jt-sistemas
```

3. **Banco de Dados**
```bash
# PostgreSQL em produção
python manage.py migrate --settings=jt_sistemas.settings.production
```

## 📈 Performance

### Otimizações Implementadas
- Query optimization com select_related e prefetch_related
- Cache com Redis
- Compressão de arquivos estáticos
- Lazy loading de imagens
- Minificação de CSS/JS

### Monitoramento
- Logs estruturados
- Métricas de performance
- Integração com Sentry (opcional)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Padrões de Código
- PEP 8 para Python
- Black para formatação
- Isort para imports
- Flake8 para linting

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Características Técnicas Destacadas

- ✅ **Arquitetura Moderna**: Django 4.2+ com boas práticas
- ✅ **UI/UX Premium**: Interface profissional e intuitiva
- ✅ **Responsividade Total**: Funciona em todos os dispositivos
- ✅ **Performance Otimizada**: Carregamento rápido e eficiente
- ✅ **Segurança Robusta**: Proteções contra vulnerabilidades comuns
- ✅ **Escalabilidade**: Preparado para crescimento
- ✅ **Manutenibilidade**: Código limpo e bem documentado
- ✅ **Testabilidade**: Estrutura preparada para testes
- ✅ **Deploy Ready**: Configurações para produção
- ✅ **API First**: Preparado para integrações futuras

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema:

- **Email**: suporte@jtsistemas.com
- **Documentação**: [docs.jtsistemas.com](https://docs.jtsistemas.com)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/jt-sistemas/issues)

---

**JT Sistemas** - Transformando a gestão empresarial com tecnologia moderna e design excepcional. 🚀