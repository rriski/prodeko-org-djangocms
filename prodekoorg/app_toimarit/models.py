from django.db import models
from django.utils.html import *


class Toimari(models.Model):

    # Toimareille ja hallituslaisille
    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.CharField(max_length=100)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def renderImage(self):
        return format_html("<img src={} />", "https://www.prodeko.org/wp-content/uploads/2017/12/anonyyyymi-uniseksi-maskulinoitu-150x150.jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name_plural = "toimarit"

class HallituksenJasen(models.Model):

    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.CharField(max_length=100)
    virka_eng = models.CharField(max_length=60)
    puhelin = models.CharField(max_length=20)
    sahkoposti = models.CharField(max_length=30)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def renderImage(self):
        return format_html("<img src={} />", "https://www.prodeko.org/wp-content/uploads/2017/12/anonyyyymi-uniseksi-maskulinoitu-150x150.jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name_plural = "hallituksen jäsenet"
