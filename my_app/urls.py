from django.conf import settings
from django.urls import path
from . import views
from django.views.static import serve

urlpatterns = [
    path("", views.index),
    path('templates/<path:template_name>', views.template_view),
    path('static/<path:path>', views.static_view),
    path("index", views.index),
    path("girisKurum", views.girisKurum, name="girisKurum"),
    path("girisEgitmen", views.girisEgitmen, name="girisEgitmen"),
    path("girisYonetici", views.girisYonetici, name="girisYonetici"),
    path("girisKullanici", views.girisKullanici, name="girisKullanici"),
    path("kayit", views.kayit),
    path("kurum", views.kurum_ana_sayfa, name="kurum"),
    path("egitmenDuzenle/<int:egitmen_id>/", views.egitmen_duzenle, name='egitmenDuzenle'),
    path("egitmen_sil/<int:egitmen_id>/", views.egitmen_sil, name='egitmen_sil'),
    path("kullanici", views.kullanici),
    path("egitmen", views.egitmen),
    path("egitmenDosyaYukle", views.egitmenDosyaYukle),
    path("egitmenSinifEkle", views.egitmenSinifEkle),
    path("egitmenOgrenciDuzenle/<int:ogrenci_id>/", views.egitmenOgrenciDuzenle, name='egitmenOgrenciDuzenle'),
    path("egitmenSinifDuzenle/<int:sinif_id>/", views.egitmenSinifDuzenle, name='egitmenSinifDuzenle'),
	path("egitmen_OgrenciSil/<int:ogrenci_id>/", views.egitmen_OgrenciSil, name='egitmen_OgrenciSil'),
    path("egitmenSinifIcerigi/<int:sinif_id>/", views.egitmenSinifIcerigi, name="egitmenSinifIcerigi"),
	path("kullaniciSinif/<int:sinif_id>/", views.kullaniciSinif, name="kullaniciSinif"),
	path("kullaniciSinifIcerik/<int:icerik_id>/", views.kullaniciSinifIcerik, name="kullaniciSinifIcerik"),
	path("egitmenSinifIcerigiSil/<int:ogrenci_id>/", views.egitmenSinifIcerigiSil, name="egitmenSinifIcerigiSil"),
	path("egitmenSinifIcerigiSil/<int:sinif_id>/<int:ogrenci_id>/", views.egitmenSinifIcerigiSil, name='egitmenSinifIcerigiSil'),
	path("egitmenSinifIcerikSil/<int:sinif_id>/<int:icerik_id>/", views.egitmenSinifIcerikSil, name='egitmenSinifIcerikSil'),
    path("egitmen_SinifSil/<int:sinif_id>/", views.egitmen_SinifSil, name='egitmen_SinifSil'),
    path("cikis", views.cikis, name="cikis"),
]
