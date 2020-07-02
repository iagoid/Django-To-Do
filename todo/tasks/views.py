from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages
import datetime


from .models import Task
#Aqui se encontram todas as funções do app tasks

#Listar todas as tarefas
@login_required
def taskList(request):
    # O search é o name do input de busca
    search = request.GET.get('search')

    #Filtro das tarefas concluidas ou não concluidas
    filter = request.GET.get('filter')

    #Informações sobre a tarefa
    #Faz a conta de quantos dias desde que foi feito o update da tarefa
    tasksDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    tasksDone = Task.objects.filter(done='done', user=request.user).count()
    tasksDoing = Task.objects.filter(done='doing', user=request.user).count()

    #Se tiver uma resposta
    if search:
        #Será filtrado peo title
        tasks = Task.objects.filter(title__icontains=search, user=request.user)

    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)

    else:
        #pega todos os objetos de Task
        #E os lista por ordem de criação
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user )

        #Atribui a classe Paginator com 3 items por page
        paginator = Paginator(tasks_list, 3)

        #Argumento que vai vir junto com a URL(/page2)
        page = request.GET.get('page')

        #Exibe o número correto de itens na página que ele está
        tasks = paginator.get_page(page)

    #retorna a list.html que esta nos templates
    return render(request, 'tasks/list.html', 
        {'tasks': tasks, 'taskrecently': tasksDoneRecently, 'tasksdone': tasksDone, 'tasksdoing': tasksDoing})

#Vear as informações da tarefa
@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

#Criar uma nove tarefa
@login_required
def newTask(request):
    #Faz a verificação se quando method é POST e assim cria a tarefa
    if request.method == 'POST':
        form = TaskForm(request.POST)

        # Faz a verificação do formulário
        if form.is_valid():
            # Para o comando de daddos e espera até ser clicado em salvar
            task = form.save(commit = False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/') 

    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

# Edit das tarefas
@login_required 
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    #Deixa o formulário preenchido com os dado criados
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        # Faz a verificação do formulário
        if form.is_valid():
            task.save()
            return redirect('/') 
        
        else:
            return render(request,'tasks/edittask.html', {'form': form, 'task': task})

    else:
        return render(request,'tasks/edittask.html', {'form': form, 'task': task})

#Delete das tarefas
@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso.')

    return redirect('/')    

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    # verifica de a tarefa está completa ou não e muda os valores
    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing' 

    task.save()

    return redirect('/')

def yourName(request, name):
    #retorna a yourname.html que esta nos templates com argumentos
    return render(request, 'tasks/yourname.html', {'name':name})
