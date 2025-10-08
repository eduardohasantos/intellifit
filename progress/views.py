from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProgressEntryForm
from .models import ProgressEntry

@login_required
def progress_page(request):
    all_entries = ProgressEntry.objects.filter(user=request.user).order_by('-date', '-id')

    if request.method == 'POST':
        form = ProgressEntryForm(request.POST)
        if form.is_valid():
            progress_entry = form.save(commit=False)
            progress_entry.user = request.user
            progress_entry.save()
            messages.success(request, 'Novo progresso salvo com sucesso!')
            return redirect('progress:progress_page')
    else:
        form = ProgressEntryForm()

    context = {
        'form': form,
        'all_entries': all_entries,
    }
    return render(request, 'progress/progress.html', context)

@login_required
def edit_progress_page(request, entry_id):
    entry_to_edit = get_object_or_404(ProgressEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = ProgressEntryForm(request.POST, instance=entry_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progresso atualizado com sucesso!')
            return redirect('progress:progress_page')
    else:
        form = ProgressEntryForm(instance=entry_to_edit)
    
    context = {
        'form': form,
        'entry_id': entry_id
    }
    return render(request, 'progress/progress_edit.html', context)

@login_required
def delete_progress_page(request, entry_id):
    entry_to_delete = get_object_or_404(ProgressEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry_to_delete.delete()
        messages.success(request, 'Registro excluído com sucesso!')
        return redirect('progress:progress_page')
    
    context = {
        'entry': entry_to_delete
    }
    return render(request, 'progress/progress_confirm_delete.html', context)