from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("",views.index),
    path('templates/<path:template_name>', views.template_view),
    path('static/<path:path>', views.static_view),
    
    path("index",views.index),
    path("girisKurum",views.girisKurum, name="girisKurum"),
    path("girisEgitmen",views.girisEgitmen, name="girisEgitmen"),
    path("girisYonetici",views.girisYonetici, name="girisYonetici"),
    path("girisKullanici",views.girisKullanici, name="girisKullanici"),
    path("kayit",views.kayit),
    path("kurum",views.kurum),
    path("kullanici",views.kullanici),
    path("egitmen",views.egitmen),
    path("egitmenDosyaYukle",views.egitmenDosyaYukle),
    path("egitmenSinifEkle",views.egitmenSinifEkle),
    path("cikis", views.cikis),
    path("videoTest", views.upload_video)
]
