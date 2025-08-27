# projeto/settings.py

import os
from pathlib import Path
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CONFIGURAÇÕES DE PRODUÇÃO E SEGURANÇA
# ==============================================================================

# Lê a chave secreta de uma variável de ambiente.
# IMPORTANTE: Em produção, o Render vai fornecer este valor.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-local-para-desenvolvimento')

# DEBUG é 'True' apenas se a variável de ambiente DEBUG for '1', caso contrário é 'False'.
DEBUG = os.environ.get('DEBUG', '0') == '1'

# Hosts permitidos. Adiciona automaticamente o host do Render quando em produção.
ALLOWED_HOSTS = [
    'www.topambiental.com',   # <-- ADICIONE SEU DOMÍNIO WWW
    'topambiental.com',     # <-- ADICIONE SEU DOMÍNIO PRINCIPAL
    '127.0.0.1',]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ==============================================================================
# APLICAÇÕES E MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestao',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Adiciona o middleware do WhiteNoise. Deve vir logo após o SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'projeto.wsgi.application'


# ==============================================================================
# BANCO DE DADOS
# ==============================================================================

# Lê a URL do banco de dados da variável de ambiente (fornecida pelo Render).
# Se não encontrar, usa o db.sqlite3 local como padrão.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# ==============================================================================
# VALIDAÇÃO DE SENHA E INTERNACIONALIZAÇÃO
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# ARQUIVOS ESTÁTICOS E DE MÍDIA
# ==============================================================================

STATIC_URL = 'static/'
# Usado para uploads de documentos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configurações para o WhiteNoise em produção
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
# OUTRAS CONFIGURAÇÕES
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL de login para administradores
LOGIN_URL = 'admin_login'



