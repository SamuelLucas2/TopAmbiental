from django.db import migrations

def create_initial_admin(apps, schema_editor):
    """
    Cria o superusuário inicial se ele ainda não existir no banco de dados.
    """
    # É a boa prática do Django obter o modelo desta forma dentro de uma migração
    User = apps.get_model('auth', 'User')
    
    # Verifica se o usuário já existe para não dar erro ao rodar a migração novamente
    if not User.objects.filter(email='samuellucas1123@gmail.com').exists():
        User.objects.create_superuser(
            username='samuel',  # Nome de usuário para login
            email='samuellucas1123@gmail.com',
            password='859589'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_admin),
    ]