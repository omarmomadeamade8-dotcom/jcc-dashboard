# website/urls.py (Certifique-se que este ficheiro está correto)

# website/urls.py (Certifique-se que este ficheiro está correto)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'), 
    path('services/', views.services, name='services'), 
    path('contact/', views.contact, name='contact'),
    path('quote-request/', views.quote_request, name='quote_request'),
    path('success/', views.success_page, name='success_page'),
    path('galeria/', views.gallery, name='gallery'),

]