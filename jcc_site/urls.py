"""
URL configuration for jcc_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# jcc_site/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # Importe 'include'
from django.conf.urls.i18n import i18n_patterns # <-- NOVO: Importe isto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')), # <--- Nova Linha para a Home Page
    path('i18n/', include('django.conf.urls.i18n')), # <-- NOVO: Adicione esta linha
]

# ... (Seu urlpatterns que já deve ter) ...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

