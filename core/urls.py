from django.urls import path
from . import views
from .views_temp import reset_admin_view, test_media_view  # VIEWS TEMPORÁRIAS

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque, name='estoque'),
    path('carro/<int:pk>/', views.detalhe_carro, name='detalhe_carro'),
    path('sobre/', views.sobre, name='sobre'),
    path('buscar/', views.buscar, name='buscar'),
    
    # VIEWS TEMPORÁRIAS - REMOVER APÓS USAR
    path('temp-reset-admin-password/', reset_admin_view, name='temp_reset_admin'),
    path('temp-test-media/', test_media_view, name='temp_test_media'),
]
