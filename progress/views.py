# Em progress/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProgressEntryForm
# Suas views antigas...
def progress_home(request):
    return render(request, 'progress/dashboard.html')

def dashboard(request):
    return render(request, 'progress/dashboard.html')

# 👇 A NOVA FUNÇÃO SUGERIDA PELO COPILOT
# Ela será executada quando a nova URL for acessada
def progress_page(request):
    if request.method == 'POST':
        # Se o formulário foi enviado (método POST)
        form = ProgressEntryForm(request.POST)
        if form.is_valid():
            # Se os dados são válidos, salve-os, mas não no banco ainda
            progress_entry = form.save(commit=False)
            # Adicione o usuário logado ao registro
            progress_entry.user = request.user
            # Agora sim, salve o objeto completo no banco de dados
            progress_entry.save()
            
            messages.success(request, 'Seu progresso foi salvo com sucesso!')
            # Redireciona para a mesma página para evitar reenvio de dados
            return redirect('progress:progress_page')
    else:
        # Se a página foi apenas acessada (método GET), crie um formulário em branco
        form = ProgressEntryForm()

    # Passamos o formulário para o template em ambos os casos (GET ou POST com erro)
    return render(request, 'progress/progress.html', {'form': form})