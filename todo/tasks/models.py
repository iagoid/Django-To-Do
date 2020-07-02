from django.db import models
from django.contrib.auth import get_user_model

class Task(models.Model):

    STATUS = (
        ('doing', 'Doing'),
        ('done', 'Done'),
    )

    #Tipo char que precisa receber argumentos
    title = models.CharField(max_length = 255)
    #Armazena mais texto
    description = models.TextField()
    #Tipo char de escolhas(0 ou 1)
    done = models.CharField(
        max_length = 5,
        choices = STATUS,
    )
    #Pega a chave estrangeira do usuario e faz o delete Cascade
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    #Data de Criação
    created_at = models.DateTimeField(auto_now_add = True)
    #Data de modificação
    updated_at = models.DateTimeField(auto_now = True)

    #Faz aparecer o titulo na página tasks do admin
    def __str__(self):
        return self.title

