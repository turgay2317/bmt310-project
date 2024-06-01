from django.db import models

class Yoneticiler(models.Model):
    yoneticiID = models.AutoField(primary_key=True)
    yoneticiEmail = models.CharField(max_length=70)
    yoneticiSifre = models.CharField(max_length=20)

class Paketler(models.Model):
    paketID = models.AutoField(primary_key=True)
    paketAdi = models.CharField(max_length=50)
    paketFiyat = models.FloatField()
    paketMaxKullanici = models.IntegerField()
    paketAciklama = models.TextField()

class Kurumlar(models.Model):
    kurumID = models.AutoField(primary_key=True)
    kurumAdi = models.CharField(max_length=255)
    kurumWebsite = models.CharField(max_length=255, blank=True, null=True)
    kurumEposta = models.EmailField(unique=True)
    kurumSifre = models.CharField(max_length=255)
    kurumPaket = models.ForeignKey('Paketler', on_delete=models.SET_NULL, null=True)
    kurumPaketSonTarih = models.DateField()
    kurumAktif = models.BooleanField(default=False)

class Egitmenler(models.Model):
    egitmenID = models.AutoField(primary_key=True)
    egitmenTamAd = models.CharField(max_length=255)
    egitmenEposta = models.EmailField(unique=True)
    egitmenSifre = models.CharField(max_length=255)
    egitmenKurum = models.ForeignKey(Kurumlar, on_delete=models.CASCADE)

class Ogrenciler(models.Model):
    ogrenciID = models.AutoField(primary_key=True)
    ogrenciTamAd = models.CharField(max_length=50)
    ogrenciKurum = models.ForeignKey(Kurumlar, on_delete=models.CASCADE)
    ogrenciFoto = models.CharField(max_length=60)
    ogrenciEposta = models.CharField(max_length=50)
    ogrenciSifre = models.CharField(max_length=50)

class Siniflar(models.Model):
    sinifID = models.AutoField(primary_key=True)
    sinifAdi = models.CharField(max_length=50)
    sinifEgitmen = models.ForeignKey(Egitmenler, on_delete=models.CASCADE)

class Icerikler(models.Model):
    icerikID = models.AutoField(primary_key=True)
    icerikAdi = models.CharField(max_length=50)
    sinif = models.ForeignKey(Siniflar, on_delete=models.CASCADE)
    icerikVideo = models.CharField(max_length=50)
    icerikPdf = models.CharField(max_length=50)

class Ogrenci_Sinif(models.Model):
    osID = models.AutoField(primary_key=True)
    ogrenci = models.ForeignKey(Ogrenciler, on_delete=models.CASCADE)
    sinif = models.ForeignKey(Siniflar, on_delete=models.CASCADE)
