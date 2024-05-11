from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponseNotFound
from my_app.models import Paketler
from .forms import KayitFormu
from .models import Kurumlar
from datetime import datetime

# Create your views here.
def index(request):
    context = {
        "paketler":Paketler.objects.all()
    }
    return render(request, "index.html", context)

def giris(request):
    return render(request,"giris.html")

def kayit(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            isletme_adi = form.cleaned_data['isletme_adi']
            web_sitesi = form.cleaned_data['web_sitesi']
            eposta = form.cleaned_data['eposta']
            sifre = form.cleaned_data['sifre']
            sozlesme = form.cleaned_data['sozlesme']
            paket = form.cleaned_data['paket']
            
            try:
                secilen_paket = Paketler.objects.get(paketID=paket)
                Kurumlar.objects.create(
                    kurumAdi=isletme_adi,
                    kurumWebsite=web_sitesi,
                    kurumEposta=eposta,
                    kurumSifre=sifre,
                    kurumPaket=secilen_paket,
                    kurumPaketSonTarih=datetime.now().date()
                )
                return redirect("giris")
            except Paketler.DoesNotExist:
                print("Hata")
        else:
            print(form.errors)

    return render(request, "kayit.html")


def kurum(request):
    return render(request, "kurum/kurumAnaSayfa.html")

def kullanici(request):
    return render(request, "kullanici/kullaniciAnaSayfa.html")

def egitmen(request):
    return render(request, "egitmen/egitmenAnaSayfa.html")

def egitmenDosyaYukle(request):
    return render(request, "egitmen/egitmenDosyaYukle.html")

def egitmenSinifEkle(request):
    return render(request, "egitmen/egitmenSinifEkle.html")


def template_view(request, template_name):
    try:
        return render(request, template_name)
    except:
        return HttpResponseNotFound("Template not found")

def static_view(request, path):
    try:
        with open(f'my_app/static/{path}', 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    except FileNotFoundError:
        return HttpResponseNotFound("Static file not found")
