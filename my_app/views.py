from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponseNotFound
from my_app.models import Paketler
from .forms import KayitFormu
from .models import Kurumlar
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
import speech_recognition as sr
import os
import moviepy.editor as mp

# Create your views here.
def index(request):
    context = {
        "paketler":Paketler.objects.all()
    }
    return render(request, "index.html", context)

def giris(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST['email']
        sifre = request.POST['sifre']

        # Veritabanında kullanıcıyı bul
        try:
            kurum = Kurumlar.objects.get(kurumEposta=email, kurumSifre=sifre)
        except Kurumlar.DoesNotExist:
            # Kullanıcı bulunamadıysa hata mesajı göster
            return render(request, 'giris.html', {'hata_mesaji': 'E-posta veya şifre yanlış.'})
        
        # Kullanıcı aktif değilse hata mesajı göster
        if not kurum.kurumAktif:
            return render(request, 'giris.html', {'hata_mesaji': 'Hesabınız aktif değil.'})

        # Kullanıcıyı oturum (session) bilgilerine ekle ve ana sayfaya yönlendir
        request.session['kurum_id'] = kurum.kurumID
        return redirect('anasayfa')  # 'anasayfa' isimli URL'ye yönlendirme yapılmalı

    return render(request, 'giris.html')
    
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