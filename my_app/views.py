from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.http import HttpResponseNotFound
from my_app.models import Paketler
from .forms import KayitFormu
from .models import Kurumlar, Siniflar
from .models import Egitmenler
from .models import Ogrenciler
from .models import Yoneticiler
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
import speech_recognition as sr
import os
import moviepy.editor as mp
from django.db import transaction


def kullaniciLoginCheck(request):
    return 'kullanici_id' in request.session

def egitmenLoginCheck(request):
    return 'egitmen_id' in request.session

def yoneticiLoginCheck(request):
    return 'yonetici_id' in request.session

def kurumLoginCheck(request):
    return 'kurum_id' in request.session

# Create your views here.
def index(request):
    context = {
        "paketler": Paketler.objects.all()
    }
    
    kullanici_adi = None
    url = None
    
    if 'kurum_id' in request.session:
        kurum_id = request.session['kurum_id']
        url = "kurum"
        try:
            kullanici_adi = Kurumlar.objects.get(kurumID=kurum_id).kurumAdi
        except Kurumlar.DoesNotExist:
            pass
    elif 'egitmen_id' in request.session:
        egitmen_id = request.session['egitmen_id']
        url = "egitmen"
        try:
            kullanici_adi = Egitmenler.objects.get(egitmenID=egitmen_id).egitmenTamAd
        except Egitmenler.DoesNotExist:
            pass
    elif 'yonetici_id' in request.session:
        yonetici_id = request.session['yonetici_id']
        url = "yonetici"
        try:
            kullanici_adi = Yoneticiler.objects.get(yoneticiID=yonetici_id).yoneticiEmail
        except Yoneticiler.DoesNotExist:
            pass
    elif 'kullanici_id' in request.session:
        ogrenci_id = request.session['kullanici_id']
        url = "kullanici"
        try:
            kullanici_adi = Ogrenciler.objects.get(ogrenciID=ogrenci_id).ogrenciTamAd
        except Ogrenciler.DoesNotExist:
            pass
    
    context['kullanici_adi'] = kullanici_adi
    context['url'] = url
    
    return render(request, "index.html", context)




def girisKurum(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST['email']
        sifre = request.POST['sifre']

        # Veritabanında kullanıcıyı bul
        try:
            kurum = Kurumlar.objects.get(kurumEposta=email, kurumSifre=sifre)
        except Kurumlar.DoesNotExist:
            # Kullanıcı bulunamadıysa hata mesajı göster
            return render(request, 'girisKurum.html', {'hata_mesaji': 'E-posta veya şifre yanlış.'})
        
        # Kullanıcı aktif değilse hata mesajı göster
        #if not kurum.kurumAktif:
            return render(request, 'girisKurum.html', {'hata_mesaji': 'Hesabınız aktif değil.'})

        # Kullanıcıyı oturum (session) bilgilerine ekle ve ana sayfaya yönlendir
        request.session['kurum_id'] = kurum.kurumID
        print(request.session.get('kurum_id'))

        return redirect('/kurum')  # 'anasayfa' isimli URL'ye yönlendirme yapılmalı

    return render(request, 'girisKurum.html')

def girisEgitmen(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST['email']
        sifre = request.POST['sifre']
       
        # Veritabanında kullanıcıyı bul
        try:
            egitmen = Egitmenler.objects.get(egitmenEposta=email, egitmenSifre=sifre)
            if egitmen:
                request.session['egitmen_id'] = egitmen.egitmenID
                return redirect("/egitmen")
        except Egitmenler.DoesNotExist:
            # Kullanıcı bulunamadıysa hata mesajı göster
            return render(request, 'girisEgitmen.html', {'hata_mesaji': 'E-posta veya şifre yanlış.'})        

        # Kullanıcıyı oturum (session) bilgilerine ekle ve ana sayfaya yönlendir

    return render(request, 'girisEgitmen.html')

def girisKullanici(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST['email']
        sifre = request.POST['sifre']

        # Veritabanında kullanıcıyı bul
        try:
            kullanici = Ogrenciler.objects.get(ogrenciEposta=email, ogrenciSifre=sifre)
            if kullanici:
                request.session['kullanici_id'] = kullanici.ogrenciID
                return redirect('/kullanici')  # 'anasayfa' isimli URL'ye yönlendirme yapılmalı
        except Ogrenciler.DoesNotExist:
            # Kullanıcı bulunamadıysa hata mesajı göster
            return render(request, 'girisKullanici.html', {'hata_mesaji': 'E-posta veya şifre yanlış.'})
        

        # Kullanıcıyı oturum (session) bilgilerine ekle ve ana sayfaya yönlendir
        

    return render(request, 'girisKullanici.html')

def girisYonetici(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST['email']
        sifre = request.POST['sifre']

        # Veritabanında kullanıcıyı bul
        try:
            yonetici = Yoneticiler.objects.get(yoneticiEmail=email, yoneticiSifre=sifre)
        except Yoneticiler.DoesNotExist:
            # Kullanıcı bulunamadıysa hata mesajı göster
            return render(request, 'girisYonetici.html', {'hata_mesaji': 'E-posta veya şifre yanlış.'})
        

        # Kullanıcıyı oturum (session) bilgilerine ekle ve ana sayfaya yönlendir
        request.session['yonetici_id'] = yonetici.yoneticiID
        return redirect('anasayfa')  # 'anasayfa' isimli URL'ye yönlendirme yapılmalı

    return render(request, 'girisYonetici.html')

    
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
                return redirect("girisKurum")
            except Paketler.DoesNotExist:
                print("Hata")
        else:
            print(form.errors)

    return render(request, "kayit.html")


def kurum(request):
    if not kurumLoginCheck(request): 
        return redirect("/")
    return render(request, "kurum/kurumAnaSayfa.html")

def kullanici(request):
    if not kullaniciLoginCheck(request): 
        return redirect("/")
    return render(request, "kullanici/kullaniciAnaSayfa.html")

def egitmen(request):
    if not egitmenLoginCheck(request): 
        return redirect("/")

    egitmen_id = request.session.get('egitmen_id')
     # Kurum bilgisini öğrenciye ata
    egitmen = Egitmenler.objects.get(egitmenID=egitmen_id)
        
    if request.method == 'POST':
        if 'sinif_ad' in request.POST:
            sinif_adi = request.POST.get('sinif_ad')
            Siniflar.objects.create(
                sinifAdi=sinif_adi,
                sinifEgitmen=egitmen
            )
        elif 'ogr_no' in request.POST:
            ogr_no = request.POST.get('ogr_no')
            ogr_ad = request.POST.get('ogr_ad')
            ogr_email = request.POST.get('ogr_email')
            ogr_sifre = request.POST.get('ogr_sifre')
            Ogrenciler.objects.create(
                ogrenciID=ogr_no,
                ogrenciTamAd=ogr_ad,
                ogrenciEposta=ogr_email,
                ogrenciSifre=ogr_sifre,
                ogrenciKurum=egitmen.egitmenKurum
            )
    
    context = {
        "ogrenciler": Ogrenciler.objects.filter(ogrenciKurum=egitmen.egitmenKurum),
        "siniflar": Siniflar.objects.filter(sinifEgitmen=egitmen)
    }
   
    return render(request, "egitmen/egitmenAnaSayfa.html",context)

def egitmenDosyaYukle(request):
    if not egitmenLoginCheck(request): 
        return redirect("/")
    return render(request, "egitmen/egitmenDosyaYukle.html")

def egitmenSinifEkle(request):
    if not egitmenLoginCheck(request): 
        return redirect("/")
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

def extract_speech_text(video_path):
    # Video dosyasını yükle
    video = mp.VideoFileClip(video_path)
    
    # Videoyu WAV formatına dönüştür
    audio_path = 'audio.wav'
    video.audio.write_audiofile(audio_path)
    
    # Sesin metne çevrilmesi için tanıma motorunu başlat
    recognizer = sr.Recognizer()
    
    # Sesin tanınması
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    # Sesin metne çevrilmesi
    try:
        text = recognizer.recognize_google(audio_data, language='tr-TR')  # Türkçe olarak tanıma yapılacak
        return text
    except sr.UnknownValueError:
        return "Ses tanınmadı"
    except sr.RequestError as e:
        return "Hata: {0}".format(e)

def upload_video(request):
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'test.mp4')
    text = extract_speech_text(video_path)
    return render(request, 'result.html', {'text': text})

def cikis(request):
    if 'kurum_id' in request.session:
        del request.session['kurum_id']
        return redirect('girisKurum')
    elif 'egitmen_id' in request.session:
        del request.session['egitmen_id']
        return redirect('girisEgitmen')
    elif 'yonetici_id' in request.session:
        del request.session['yonetici_id']
        return redirect('girisYonetici')
    elif 'kullanici_id' in request.session:
        del request.session['kullanici_id']
        return redirect('girisKullanici')
    



def kurum_ana_sayfa(request):
    # Kullanıcı oturum açmış mı kontrol et
    if 'kurum_id' in request.session:
        kurum_id = request.session['kurum_id']
        try:
            kurum = Kurumlar.objects.get(kurumID=kurum_id)
            if request.method == 'POST':
                tam_ad = request.POST.get('tam_ad')
                email = request.POST.get('email')
                sifre = request.POST.get('sifre')
                if kurum_id:
                    Egitmenler.objects.create(
                        egitmenTamAd=tam_ad,
                        egitmenEposta=email,
                        egitmenSifre=sifre,
                        egitmenKurum=kurum
                    )

            paket_bilgisi = kurum.kurumPaket
            ogretmen_sayisi = Egitmenler.objects.filter(egitmenKurum=kurum).count()
            ogrenci_sayisi = Ogrenciler.objects.filter(ogrenciKurum=kurum).count()
            egitmenler = Egitmenler.objects.filter(egitmenKurum=kurum)
            
            context = {
                'kurum': kurum,
                'paket_bilgisi': paket_bilgisi,
                'ogretmen_sayisi': ogretmen_sayisi,
                'ogrenci_sayisi': ogrenci_sayisi,
                'egitmenler': egitmenler,
            }

            return render(request, 'kurum/kurumAnaSayfa.html', context)
        except Kurumlar.DoesNotExist:
            pass
    
    return redirect('girisKullanici')  # Kullanıcı oturum açmamışsa giriş sayfasına yönlendir

def egitmen_duzenle(request, egitmen_id):
    egitmen = get_object_or_404(Egitmenler, egitmenID=egitmen_id)
    if request.method == 'POST':
        egitmen.egitmenTamAd = request.POST.get('tam_ad')
        egitmen.egitmenEposta = request.POST.get('email')
        egitmen.egitmenSifre = request.POST.get('sifre')
        egitmen.save()
        return redirect('kurum')
    return render(request, 'kurum/egitmenDuzenle.html', {'egitmen': egitmen})

def egitmenOgrenciDuzenle(request, ogrenci_id):
    ogrenci = get_object_or_404(Ogrenciler, ogrenciID=ogrenci_id)
    if request.method == 'POST':
        ogrenci.ogrenciID = request.POST.get('ogr_no')
        ogrenci.ogrenciTamAd = request.POST.get('ogr_ad')
        ogrenci.ogrenciEposta = request.POST.get('ogr_email')
        ogrenci.ogrenciSifre = request.POST.get('ogr_sifre')
        ogrenci.save()
        return redirect('/egitmen')
    return render(request, 'egitmen/egitmenOgrenciDuzenle.html', {'ogrenci': ogrenci})

def egitmen_sil(request, egitmen_id):
    egitmen = get_object_or_404(Egitmenler, egitmenID=egitmen_id)
    egitmen.delete()
    return redirect('kurum')

def egitmen_OgrenciSil(request, ogrenci_id):
    ogrenci = get_object_or_404(Ogrenciler, ogrenciID=ogrenci_id)
    ogrenci.delete()
    return redirect("/egitmen")

def egitmen_SinifSil(request, sinif_id):
    sinif = get_object_or_404(Siniflar, sinifID=sinif_id)
    sinif.delete()
    return redirect("/egitmen")

def egitmenSinifIcerigi(request, sinif_id):
    sinif = get_object_or_404(Siniflar, sinifID=sinif_id)
   
    return render(request, 'egitmen/egitmenSinifIcerigi.html', {'sinif': sinif})

def egitmenSinifDuzenle(request, sinif_id):
    sinif = get_object_or_404(Siniflar, sinifID=sinif_id)
    if request.method == 'POST':
        sinif.sinifAdi = request.POST.get('sinif_ad')
        sinif.save()
        return redirect('/egitmen')
    return render(request, 'egitmen/egitmenSinifDuzenle.html', {'sinif': sinif})

    