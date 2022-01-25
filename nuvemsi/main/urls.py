from django.urls import path
from . import views
#Sayfa urllerini tanımladığımız kısım.
urlpatterns = [
    path("", views.home, name="home"),
    path("Home", views.home, name="home"),
    path("ResimYukle", views.uploadimg, name="uploadimg"),
    path("BelgeYukle", views.uploaddoc, name="uploaddoc"),
    path("logout", views.logout_request, name="logout"),
    path("delete/<str:pk>", views.delete_request, name="delete"),
    path("download/<str:pk>", views.download_request, name="download"),
    path("Dokuman", views.doclist_request, name="doclist"),
    path("DokumanDownload/<str:pk>", views.docdown_request, name="downloaddoc"),
    path("DokumanDelete/<str:pk>", views.deldoc_request, name="deletedoc"),
    
]