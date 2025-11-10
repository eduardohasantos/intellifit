# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from notes.forms import editNotesForm
from django.contrib import messages

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

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    context = {
        'note': note
    }
    return render(request, 'notes/note_detail.html', context)

@login_required
def edit_notes(request, pk):
    selected_note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Passa request.POST e a instância para o formulário
        form = editNotesForm(request.POST, instance=selected_note)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Nota editada com sucesso!")
            return redirect("notes:note_list")  # Nome da URL, não caminho do HTML
    else:
        # GET: Renderiza o formulário com os dados atuais
        form = editNotesForm(instance=selected_note)
    
    context = {
        'note': selected_note,
        'form': form
    }
    return render(request, 'notes/edit_notes.html', context)

@login_required
def delete_notes(request, pk):
    selected_note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        selected_note.delete()
        messages.success(request, "Anotação removida com sucesso!")
        return redirect("notes:note_list")  # Nome da URL, não caminho do HTML
    
    context = {
        'note': selected_note
    }
    return render(request, 'notes/delete_notes.html', context)