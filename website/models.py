from django.db import models

# Modelo 1: Serviço (Service)
class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title

# Modelo 2: Projeto (Project) - VERSÃO ÚNICA E CORRETA
class Project(models.Model):
    title = models.CharField(max_length=200)
    # Exemplo: Construção Nova, Remodelação, etc.
    category = models.CharField(max_length=100) 
    location = models.CharField(max_length=250)
    description = models.TextField()
    # Campo de Imagem - O Render usará o storage configurado no settings.py
    image = models.ImageField(upload_to='portfolio_images/') 
    date_completed = models.DateField(null=True, blank=True, verbose_name="Data de Conclusão")
    
    class Meta:
        # Garante que os projetos mais recentes aparecem primeiro
        ordering = ['-date_completed'] 
    
    def __str__(self):
        return self.title
    
# Modelo 3: Imagens da Galeria (GalleryImage)
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