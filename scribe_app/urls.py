from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='home'), 
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('record_voice/', views.record_voice_view, name='record_voice'),
    path('show_hpi/<int:pdf_id>/', views.show_hpi, name='show_hpi'),
]
