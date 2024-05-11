<h2>ENV Kurulumu ve Çalıştırılması</h2>
<ol>
   <li>
     "python -m venv myenv" komutu ile myenv adında bir environment oluşturuyoruz.
  </li>
  <li>
    <p>Aktivite etme</p>
    <p>* Windows : eogrenmesistemi\Scripts\activate.bat</p>
    <p>MacOS : source eogrenmesistemi/Scripts/activate</p>
  </li>
  <li>
    pip install django==3.2.9
  </li>
  <li>
    "pip freeze" ile yüklenmiş mi kontrol et.
  </li>
  <li>
    Çıkmak istersen deactivate
  </li>
  <li>
    İÇİNDEYKEN PROGRAMI ÇALIŞTIRMAK İÇİN: "python manage.py runserver"
  </li>
</ol>

<h2>PROJE KLASÖR YAPISI</h2>
<ul>
  <li><b>static</b> : image, js, css dosyaları için</li>
  <li><b>templates</b> : html dosyaları için</li>
  <li><b>media</b> : user media için</li>
</ul>
