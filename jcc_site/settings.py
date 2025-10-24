import os
from pathlib import Path

# Definição padrão do BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# --- DADOS DA EMPRESA (CONTEXTO PARA TEMPLATES) ---
COMPANY_EMAIL = 'contact@jccconstrucoes.co.mz'
COMPANY_PHONE = '+258 84 123 4567'
COMPANY_ADDRESS = 'Av. Principal 123, Maputo, Moçambique'
SOCIAL_FACEBOOK = 'https://facebook.com/jccconstrucoes'
SOCIAL_LINKEDIN = 'https://linkedin.com/company/jccconstrucoes'

# --- CONFIGURAÇÕES DE AMBIENTE ---
SECRET_KEY = 'django-insecure-4bs_f@(*)!yqw5ey(7mbvy9dee7=+81j-y)@tuoe%+f&(17e35'

# MODO DE DESENVOLVIMENTO
DEBUG = True
# Adicione aqui o domínio do Render para permitir acesso
ALLOWED_HOSTS = ['jcc-juridio-chicala-construcoes.onrender.com', 'localhost', '127.0.0.1']

    # IMPORTANTE: Se você tiver um ficheiro .env para variáveis SECRET_KEY ou DEBUG, use-o
    # para definir esta lista de forma dinâmica em vez de codificar.
    # Mas para o propósito do deploy no Render, esta correção direta é necessária.

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'website', 
]

# --- MIDDLEWARE (COM ORDEM CORRETA) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.locale.LocaleMiddleware', # Para a gestão de idiomas
    
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

# --- BASE DE DADOS ---
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
LANGUAGE_CODE = 'pt-pt'# Definir Português como o idioma padrão
TIME_ZONE = 'Africa/Maputo' # Recomendo fuso horário de Moçambique
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('pt', 'Português'),
    ('en', 'English'),
    ('fr', 'Français'), 
    ('es', 'Español'), 
    ('ar', 'العربية'), 
    ('de', 'Deutsch'), 
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# --- FICHEIROS ESTÁTICOS E MEDIA ---
STATIC_URL = 'static/' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]

STATIC_ROOT = BASE_DIR / 'staticfiles' # <-- ESSENCIAL PARA PRODUÇÃO!

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURAÇÃO DE EMAIL ---
# Modo de Desenvolvimento: Envia emails para a consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

# Para DEPLOYMENT, mude:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.seuservidor.co.mz'
# (Adicionar as outras credenciais SMTP)

DEFAULT_FROM_EMAIL = COMPANY_EMAIL
SERVER_EMAIL = COMPANY_EMAIL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'