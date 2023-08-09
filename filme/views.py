from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHome

# Create your views here.
# def homepage(request):
#     return render(request, 'homepage.html')

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHome

    def get(self, request, *args: Any, **kwargs: Any):

        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) # redireciona o usuario para a url final
        
    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

# # class based view
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, 'homefilmes.html', context)

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_list

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object

    def get(self, request, *args: Any, **kwargs: Any):
        # descobrir qual o filme o usuario esta acessando
        filme = self.get_object()
        #somar 1 ao numero de visualizacoes
        filme.visualizacoes += 1
        # salvar o filme
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super(Detalhesfilme, self).get(request, *args, **kwargs) # redireciona o usuario para a url final

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # Filtrar a minha lista de filmes pelo genero do filme atual
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context
    
class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self) -> QuerySet[Any]:
        # pegar o valor do campo de pesquisa
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            # filtrar a lista de filmes com base no termo de pesquisa
            Object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return Object_list
        else:
            return None
        
class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')