from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("",views.index),
    path('templates/<path:template_name>', views.template_view),
    path('static/<path:path>', views.static_view),
    
    path("index",views.index),
    path("giris",views.giris),
]
