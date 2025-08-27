from django.db import models


# A importação 'os' não é mais necessária, pois removemos a função de caminho local.

class Cliente(models.Model):
    """
    Representa um cliente (posto de gasolina) no sistema.
    """
    nome_empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, help_text="Formato: XX.XXX.XXX/XXXX-XX")
    senha = models.CharField(max_length=128) # A senha é armazenada com hash pela view

    def __str__(self):
        return self.nome_empresa


# A função 'get_upload_path' foi removida, pois agora o Cloudinary gerencia
# o caminho dos arquivos enviados.


class Documento(models.Model):
    """
    Representa um documento enviado para um cliente específico.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='documentos')
    titulo = models.CharField(max_length=200)

    # Armazena PDFs/arquivos localmente no servidor
    arquivo = models.FileField(upload_to='documentos/')

    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo