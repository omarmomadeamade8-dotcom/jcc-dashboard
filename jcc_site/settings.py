import os
from pathlib import Path
import dj_database_url

# Definição padrão do BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# --- DADOS DA EMPRESA (CONTEXTO PARA TEMPLATES) ---
COMPANY_EMAIL = 'juridio@jcconstrucoes.co.mz ou geral@jcconstrucoes.co.mz'
COMPANY_PHONE = '+258 84 123 4567'
COMPANY_ADDRESS = 'Av. Principal 123, Maputo, Moçambique'
SOCIAL_FACEBOOK = 'https://facebook.com/jccconstrucoes'
SOCIAL_LINKEDIN = 'https://linkedin.com/company/jccconstrucoes'

# --- CONFIGURAÇÕES DE AMBIENTE ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4bs_f@(*)!yqw5ey(7mbvy9dee7=+81j-y)@tuoe%+f&(17e35')

# MODO DE PRODUÇÃO NO RENDER - ESSENCIAL PARA WHITENOISE
DEBUG = False 
# Hosts permitidos para o Render
ALLOWED_HOSTS = ['jcc-juridio-chicala-construcoes.onrender.com', 'localhost', '127.0.0.1']

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'website', 
    # django-storages não é mais estritamente necessário para esta solução,
    # mas se o usarmos no futuro, deve estar aqui.
]

# --- MIDDLEWARE (COM ORDEM CORRETA PARA WHITENOISE) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WHITENOISE: Adicionado aqui, logo abaixo do SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.locale.LocaleMiddleware', 
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- TEMPLATES ---
ROOT_URLCONF = 'jcc_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'jcc_site.wsgi.application'

# --- BASE DE DADOS (CONFIGURAÇÃO PostgreSQL/SQLite Dinâmica) ---
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
        )
    }
else:
    # Caso contrário, usa SQLite localmente (para desenvolvimento)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Africa/Maputo'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('pt', 'Português'), ('en', 'English'), ('fr', 'Français'), 
    ('es', 'Español'), ('ar', 'العربية'), ('de', 'Deutsch'), 
]

LOCALE_PATHS = [ BASE_DIR / 'locale', ]

# ------------------------------------------------------------------
# CONFIGURAÇÕES FINAIS DE FICHEIROS ESTÁTICOS E MEDIA (CORRIGIDO)
# ------------------------------------------------------------------

# 1. Configuração de STATIC FILES para Produção
STATIC_URL = '/static/' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]
# CRÍTICO: O WhiteNoise recolhe daqui
STATIC_ROOT = BASE_DIR / 'staticfiles' 

# CORREÇÃO CRÍTICA: Remove a linha que causava conflito com ImageField em DEBUG=False
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

# 2. Configuração de MEDIA FILES (Imagens dos Modelos)
MEDIA_URL = '/media/'
# O Render NÃO suporta media files (imagens do utilizador) sem S3, mas o Django precisa que exista.
MEDIA_ROOT = BASE_DIR / 'media'

# 3. Middleware de Segurança (Para Render)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True # Força o HTTPS

# --- CONFIGURAÇÃO DE EMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
DEFAULT_FROM_EMAIL = COMPANY_EMAIL
SERVER_EMAIL = COMPANY_EMAIL
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'