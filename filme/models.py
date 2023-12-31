from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

LISTA_CATEGORIAS = (
    ("ANALISES", 'Analises'),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros"),
)

# Criar o Filme
class Filme(models.Model):
    # - thumb
    thumb = models.ImageField(upload_to='thumb_filmes')
    # - título
    titulo = models.CharField(max_length=100)
    # - sinopse
    sinopse = models.TextField(max_length=1000)
    # - Categoria
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    # - Quantidade de views
    visualizacoes = models.IntegerField(default=0)
    # - data de Criação
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.titulo
    
# Criar os Epsoódios
class Epsodio(models.Model):
    filme = models.ForeignKey("Filme", on_delete=models.CASCADE, related_name="episodios")
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + ' - '+ self.titulo



# Criar o Usuário
class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")