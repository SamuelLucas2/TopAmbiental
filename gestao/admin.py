# gestao/admin.py
from django.contrib import admin
from .models import Cliente, Documento

admin.site.register(Cliente)
admin.site.register(Documento)