# notes/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    context = {
        'notes': notes
    }
    return render(request, 'notes/note_list.html', context)

@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            return redirect('notes:note_list')
    
    return render(request, 'notes/note_form.html')

# ADICIONE A FUNÇÃO ABAIXO
@login_required
def note_detail(request, pk):
    # Busca a anotação pelo ID (pk) E garante que ela pertence ao usuário logado
    note = get_object_or_404(Note, pk=pk, user=request.user)
    context = {
        'note': note
    }
    return render(request, 'notes/note_detail.html', context)