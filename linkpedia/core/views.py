from django.shortcuts import render, redirect
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