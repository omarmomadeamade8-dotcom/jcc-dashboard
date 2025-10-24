# website/models.py
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200) 
    description = models.TextField() 
    location = models.CharField(max_length=100) 
    completion_date = models.DateField() 
    image = models.ImageField(upload_to='project_images/') 

    def __str__(self):
        return self.title

# website/models.py

# O seu modelo de Serviço (se já o tiver)
class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title

# NOVO MODELO: Projeto
class Project(models.Model):
    title = models.CharField(max_length=200)
    # Exemplo: Construção Nova, Remodelação, etc.
    category = models.CharField(max_length=100) 
    location = models.CharField(max_length=250)
    description = models.TextField()
    # Adicionar a imagem. O upload_to cria uma subpasta dentro de static/media
    image = models.ImageField(upload_to='portfolio_images/') 
    date_completed = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
# website/models.py

# ... (Seu modelo Service) ...

# ... (Seu modelo Project) ...

# NOVO MODELO: Imagens da Galeria
class GalleryImage(models.Model):
    caption = models.CharField(max_length=250, null=True, blank=True, verbose_name="Legenda da Imagem")
    image = models.ImageField(upload_to='gallery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagem da Galeria"
        verbose_name_plural = "Imagens da Galeria"
        ordering = ['-uploaded_at'] # Ordena pela mais recente

    def __str__(self):
        return self.caption or f"Imagem #{self.id}"