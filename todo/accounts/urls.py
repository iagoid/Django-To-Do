from django.urls import path
from . import views

#Aqui são definidas quais URL o app tasks pode acessar e qual função ele chama
urlpatterns = [
    
    #nome da URL, caminho.nomefunção
    path('register/', views.SignUp.as_view(), name="SignUp")
]

#localhost:8000 / URL do Arquivo Principal / essa URL