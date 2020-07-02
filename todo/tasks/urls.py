from django.urls import path
from . import views

#Aqui são definidas quais URL o app tasks pode acessar e qual função ele chama
urlpatterns = [
    
    #nome da URL, caminho.nomefunção
    path('', views.taskList, name='task-list'),
    path('tasks/<int:id>', views.taskView, name="task-view"),
    path('newtask/', views.newTask, name="new-task"),
    path('edit/<int:id>', views.editTask, name='edit-task'),
    path('changestatus/<int:id>', views.changeStatus, name='change-status'),
    path('delete/<int:id>', views.deleteTask, name="delete-task"),
    path('yourname/<str:name>', views.yourName),

]

#localhost:8000 / URL do Arquivo Principal / essa URL