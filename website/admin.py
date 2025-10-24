# website/admin.py

from django.contrib import admin
from .models import Project  # Importe o modelo Project que criamos
from .models import Service, Project # Importe o novo modelo
from .models import Service, Project, GalleryImage

# 1. Registra o modelo Project
admin.site.register(Project)

# website/admin.py
# O seu registo de Service (se já o tiver)
admin.site.register(Service) 

admin.site.register(GalleryImage)

