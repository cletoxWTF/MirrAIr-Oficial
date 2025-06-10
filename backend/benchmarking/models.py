from django.db import models

# MODELO DE TRADUCCIÓN

class Traduction(models.Model):
    #AQUI AGREGAR IMAGEN EN CASO DE NECESITAR
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    score = models.IntegerField(verbose_name="Calificación")
    votes = models.IntegerField(verbose_name="Votos Totales")
    finalScore = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Calificación Final")

    class Meta:
        verbose_name = "Traducción"
        verbose_name_plural = "Traducciones"
        ordering = ['name']

    def __str__(self):
        return self.name
