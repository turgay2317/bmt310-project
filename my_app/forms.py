from django import forms
from my_app.models import Video

class KayitFormu(forms.Form):
    isletme_adi = forms.CharField(max_length=100)
    web_sitesi = forms.URLField()
    eposta = forms.EmailField()
    sifre = forms.CharField(widget=forms.PasswordInput)
    paket = forms.ChoiceField(choices=[(1, ''), (2, ''), (3, '')], widget=forms.RadioSelect)
    sozlesme = forms.BooleanField(label='Sözleşmeyi Kabul Ediyorum')

class OgrenciForm(forms.ModelForm):
    class Meta:
        fields = ['ogrenciID', 'ogrenciTamAd', 'ogrenciEposta', 'ogrenciSifre'] 

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
