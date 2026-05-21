from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import LinkModel
from .forms import LinkForm

def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)

@login_required
def create(request):
    if(request.method == 'POST'):
        # Informando meu form
        form = LinkForm(request.POST)
        
        # Validando as informações enviadas
        if form.is_valid():
            # Salvando no banco
            form.save()
            # Redirecionando para a home page
            return redirect(home)
        else:
            print(form.errors)
        
    else:
        # Se der errado, ele me devolve meu próprio form vazio
        form = LinkForm()
        

    # Enviando o form na requisição
    return render(request, 'create.html', { 'form': form })

@login_required
def all(request):
    allLinks = LinkModel.objects.all()

    return render(request, 'table.html', { 'links': allLinks })

@login_required
def delete(request, id):
    # Capturando o objeto através do ID, mas se ele não encontrar, me retorna 404
    link = get_object_or_404(
        LinkModel,
        id=id
    )

    # Deletando se achar a instancia no banco
    link.delete()

    return redirect('table')

@login_required
def edit(request, id):
    # Capturar o objeto no banco de dados
    link = LinkModel.objects.get(id=id)

    if request.method == 'POST':
        # Parametrizando meu linkform
        form = LinkForm(
            request.POST,
            instance=link # Mantendo meu objeto atual com as informações que vieram do banco
        )

        # Validando o formulário
        if form.is_valid():
            form.save()
            return redirect('table')

    # Matendo a minha instancia no banco intacta em caso de erro
    else:
        form = LinkForm(instance=link)
    
    return render(request, 'edit.html', { 'form': form })
