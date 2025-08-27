# projeto/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls), # Opcional: admin padrão do Django
    path('', include('gestao.urls')), # <-- INCLUI AS ROTAS DO NOSSO APP
]

# Adiciona a rota para servir os arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)