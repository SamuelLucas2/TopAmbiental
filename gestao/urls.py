# gestao/urls.py - VERSÃO FINAL E CORRETA
# VERSÃO FINAL E CORRETA - 24/08/2025
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rota raiz do site aponta para a landing page
    path('', views.landing_page, name='home'),

    #download
    path('download/<int:doc_id>/', views.download_documento, name='download_documento'),


    # Autenticação
    path('login/admin/', views.admin_login_view, name='admin_login'),
    path('login/cliente/', views.client_login_view, name='client_login'),
    path('logout/admin/', views.user_logout, name='admin_logout'),
    path('logout/cliente/', views.client_logout_view, name='client_logout'),

    # Painel Cliente
    path('cliente/dashboard/', views.cliente_dashboard, name='client_dashboard'),

    # Upload de documento
    path('upload/', views.upload_documento, name='upload_documento'),

    # Painel Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/clientes/', views.client_list, name='client_list'),
    path('admin/clientes/novo/', views.client_create, name='client_create'),
    path('admin/clientes/<int:pk>/editar/', views.client_update, name='client_update'),
    path('admin/clientes/<int:pk>/excluir/', views.client_delete, name='client_delete'),
    path('admin/clientes/<int:pk>/', views.client_detail, name='client_detail'),
    path('admin/documentos/<int:doc_pk>/excluir/', views.delete_document, name='delete_document'),
    path('admin/usuarios/', views.user_list, name='user_list'),
    path('admin/usuarios/novo/', views.user_create, name='user_create'),
    path('admin/usuarios/<int:pk>/excluir/', views.user_delete, name='user_delete'),

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)