# gestao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Cliente, Documento
from .forms import AdminLoginForm, ClientLoginForm, ClienteForm, DocumentoForm, UserForm
from django.shortcuts import render # Garanta que 'render' está importado
from django.db.models import Count
from django.contrib import messages
from .forms import DocumentoForm
from django.http import FileResponse, Http404
from .models import Documento

# Helpers
def is_admin(user):
    return user.is_authenticated and user.is_staff

def upload_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Documento enviado com sucesso!")
            return redirect('client_dashboard')
    else:
        form = DocumentoForm()
    return render(request, 'upload.html', {'form': form})

@user_passes_test(is_admin)
def client_list(request):
    # MUDANÇA: Usamos .annotate() para contar os documentos de cada cliente
    clientes = Cliente.objects.annotate(
        doc_count=Count('documentos')
    ).order_by('nome_empresa')
    
    return render(request, 'admin_panel/client_list.html', {'clientes': clientes})

# --- Autenticação ---
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # O Django autentica usando 'username', então buscamos o user pelo email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None and user.is_staff:
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Credenciais de administrador inválidas.")
            except User.DoesNotExist:
                messages.error(request, "Administrador não encontrado.")
    else:
        form = AdminLoginForm()
    return render(request, 'auth/admin_login.html', {'form': form})

def landing_page(request):
    return render(request, 'landing_page.html')

def client_login_view(request):
    if 'cliente_id' in request.session:
        return redirect('client_dashboard')

    if request.method == 'POST':
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            cnpj = form.cleaned_data['cnpj']
            senha = form.cleaned_data['senha']
            try:
                cliente = Cliente.objects.get(cnpj=cnpj)
                if check_password(senha, cliente.senha):
                    request.session['cliente_id'] = cliente.id
                    return redirect('client_dashboard')
                else:
                    messages.error(request, "CNPJ ou senha inválidos.")
            except Cliente.DoesNotExist:
                messages.error(request, "CNPJ ou senha inválidos.")
    else:
        form = ClientLoginForm()
    return render(request, 'auth/client_login.html', {'form': form})
    
def user_logout(request):
    logout(request)
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    messages.success(request, "Você saiu com segurança.")
    return redirect('admin_login')

# --- Painel do Administrador ---
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_clientes = Cliente.objects.count()
    total_docs = Documento.objects.count()
    return render(request, 'admin_panel/dashboard.html', {'total_clientes': total_clientes, 'total_docs': total_docs})

# CRUD de Clientes
@user_passes_test(is_admin)
def client_list(request):
    clientes = Cliente.objects.all().order_by('nome_empresa')
    return render(request, 'admin_panel/client_list.html', {'clientes': clientes})

@user_passes_test(is_admin)
def client_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.senha = make_password(form.cleaned_data['senha'])
            cliente.save()
            messages.success(request, f"Cliente '{cliente.nome_empresa}' criado com sucesso!")
            return redirect('client_list')
    else:
        form = ClienteForm()
    return render(request, 'admin_panel/client_form.html', {'form': form, 'title': 'Cadastrar Novo Cliente'})

@user_passes_test(is_admin)
def client_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            updated_cliente = form.save(commit=False)
            if form.cleaned_data['senha']:
                updated_cliente.senha = make_password(form.cleaned_data['senha'])
            else:
                updated_cliente.senha = cliente.senha # Mantém a senha antiga se o campo estiver vazio
            updated_cliente.save()
            messages.success(request, "Dados do cliente atualizados com sucesso!")
            return redirect('client_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'admin_panel/client_form.html', {'form': form, 'title': 'Editar Cliente', 'edit_mode': True})

@user_passes_test(is_admin)
def client_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        nome_cliente = cliente.nome_empresa
        cliente.delete()
        messages.success(request, f"Cliente '{nome_cliente}' excluído com sucesso.")
        return redirect('client_list')
    return render(request, 'admin_panel/client_confirm_delete.html', {'cliente': cliente})


        documentos = cliente.documentos.all().order_by('-data_envio')
        return render(request, 'client_panel/dashboard.html', {'cliente': cliente, 'documentos': documentos})
        
    except Cliente.DoesNotExist:
        if 'cliente_id' in request.session:
            del request.session['cliente_id']
        messages.error(request, "Sua sessão era inválida. Por favor, faça o login novamente.")
        return redirect('client_login')

        documentos = cliente.documentos.all().order_by('-data_envio')
        return render(request, 'client_panel/dashboard.html', {'cliente': cliente, 'documentos': documentos})
        
    except Cliente.DoesNotExist:
        if 'cliente_id' in request.session:
            del request.session['cliente_id']
        messages.error(request, "Sua sessão era inválida. Por favor, faça o login novamente.")
        return redirect('client_login')

def download_documento(request, doc_id):
    # Verifica se o cliente está logado via sessão
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('client_login')  # se não tiver sessão, manda pro login do cliente

    try:
        cliente = Cliente.objects.get(pk=cliente_id)
        doc = Documento.objects.get(id=doc_id, cliente=cliente)

        # Extrai o nome original do arquivo salvo
        nome_arquivo = doc.arquivo.name.split('/')[-1]  

        return FileResponse(
            doc.arquivo.open('rb'),
            as_attachment=True,
            filename=nome_arquivo
        )
    except (Cliente.DoesNotExist, Documento.DoesNotExist):
        raise Http404("Documento não encontrado")

    
# Detalhes do Cliente e Gestão de Documentos
@user_passes_test(is_admin)
def client_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    documentos = cliente.documentos.all().order_by('-data_envio')
    
    if request.method == 'POST':
        doc_form = DocumentoForm(request.POST, request.FILES)
        if doc_form.is_valid():
            documento = doc_form.save(commit=False)
            documento.cliente = cliente
            documento.save()
            messages.success(request, f"Documento '{documento.titulo}' enviado com sucesso!")
            return redirect('client_detail', pk=pk)
    else:
        doc_form = DocumentoForm()
        
    return render(request, 'admin_panel/client_detail.html', {'cliente': cliente, 'documentos': documentos, 'doc_form': doc_form})

@user_passes_test(is_admin)
def delete_document(request, doc_pk):
    documento = get_object_or_404(Documento, pk=doc_pk)
    cliente_pk = documento.cliente.pk
    if request.method == 'POST':
        nome_doc = documento.titulo
        documento.arquivo.delete(save=True) # Remove o arquivo físico
        documento.delete()
        messages.success(request, f"Documento '{nome_doc}' excluído com sucesso.")
    return redirect('client_detail', pk=cliente_pk)

# Gestão de usuários Admin
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.filter(is_staff=True).order_by('username')
    return render(request, 'admin_panel/user_list.html', {'users': users})

@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.is_superuser = True # Para acesso total
            user.save()
            messages.success(request, f"Administrador '{user.username}' criado com sucesso!")
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_form.html', {'form': form})
    
@user_passes_test(is_admin)
def user_delete(request, pk):
    user_to_delete = get_object_or_404(User, pk=pk)
    if request.user == user_to_delete:
        messages.error(request, "Você não pode excluir sua própria conta.")
        return redirect('user_list')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"Administrador '{username}' excluído com sucesso.")
        return redirect('user_list')
        
    return render(request, 'admin_panel/user_confirm_delete.html', {'user_to_delete': user_to_delete})


# --- Área do Cliente ---
def cliente_dashboard(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, "Acesso não autorizado. Por favor, faça o login.")
        return redirect('client_login')
        
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    documentos = cliente.documentos.all().order_by('-data_envio')
    
    return render(request, 'client_panel/dashboard.html', {'cliente': cliente, 'documentos': documentos})

def client_logout_view(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    messages.success(request, "Você saiu com segurança.")
    return redirect('client_login')

    