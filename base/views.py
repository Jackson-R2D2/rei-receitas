from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Q
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Revenue, Message
from .forms import RegisterUserForm, RevenueForm
from django.core.paginator import Paginator
from django.db.models import Max
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

class Home(ListView):
    template_name = 'base/home.html'
    model = Revenue
    recipes = {'main_recipe':Revenue.objects.get(id = 4), 'recipe_right_top':Revenue.objects.get(id = 5), 'recipe_right_down':Revenue.objects.get(id = 2),'bolo_fuba':Revenue.objects.get(id = 1), 'bolo':Revenue.objects.get(id = 6), 'poke':Revenue.objects.get(id = 7)}
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.recipes
        context['featured_users'] = get_user_model().objects.annotate(max_date=Max('revenue')).all().order_by('-max_date')[:3]
        return context


class RevenuePage(View):

    def __init__(self):
        self.template_name = 'base/revenuePage.html'
        self.functionalities = {'button_feedback':self.modify_button_feedback, 'comment':self.save_message}


    def get(self, request, *args, **kwargs):
        self.revenue = Revenue.objects.get(id = kwargs['pk'])
        self.like_buttom = self.get_like_or_deslike(request)
        return render(request, self.template_name, {'revenue':self.revenue, 'like_buttom':self.like_buttom})

    
    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):    
        self.revenue = Revenue.objects.get(id = kwargs['pk'])
        self.like_buttom = self.get_like_or_deslike(request)
        self.load_funcionalities(request)
        return render(request, self.template_name, {'revenue':self.revenue, 'like_buttom':self.like_buttom})


    def load_funcionalities(self, request):
    # Aqui será carregado uma das funções que está no atributo functionalities
        for funcionalitie in self.functionalities:
            if request.POST.get(funcionalitie) != None:
                self.functionalities[funcionalitie](request)


    def add_many_to_many(self, request, object):
        # Adiciona um objeto no (no caso user) no atributo like
        object.like.add(request.user)

    
    def remove_many_to_many(self, request, object):
        # Remove um objeto no (no caso user) no atributo like
        object.like.remove(request.user)

    
    def modify_button_feedback(self, request):
        # Modifica o atributo like
        if self.like_buttom == 'like':
            self.add_many_to_many(request, self.revenue)
            self.like_buttom = 'deslike'
        else:
            self.remove_many_to_many(request, self.revenue)
            self.like_buttom = 'like'        


    def get_like_or_deslike(self, request):
        # Retorna um valor 'like' ou 'deslike' para o atributo like_buttom 
        if request.user in self.revenue.like.all():
            return 'deslike'
        else:
            return 'like'

    
    def save_message(self, request):
        # Cria e salva a mensagem
        message = Message.objects.create(
            host = request.user,
            revenue = self.revenue,
            textMessage = request.POST.get('comment')
        )
        message.save()


class RegisterRevenue(View):
    template_name = 'base/register_revenue.html'
    form_class = RevenueForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form':self.form_class})

    
    def post(self, request, *args, **kwargs):
        self.form_class = RevenueForm(request.POST, request.FILES)
        if self.form_class.is_valid():
            revenue = self.form_class.save(commit=False)
            revenue.host = request.user
            revenue.save()
            return redirect('/')


class RegisterUser(View):
    template_name = 'base/login.html'
    registration_sistem = 'register'
    form_class = RegisterUserForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'registration_sistem':self.registration_sistem, 'form':self.form_class})

    
    def post(self, request, *args, **kwargs):
        self.form_class = RegisterUserForm(request.POST, request.FILES)
        if self.form_class.is_valid():
            if self.form_class.verify_password(self.form_class.cleaned_data.get('password')):
                messages.error(request, self.form_class.error)
            else:
                user = self.form_class.save(commit=False)
                user.save()
                login(request, user, backend='account.backend.CustomBackend')
                return redirect('/')
        return render(request, self.template_name, {'registration_sistem':self.registration_sistem, 'form':self.form_class})


class UserPage(View):
    template_name = 'base/userPage.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'revenues': request.user.revenue_set.all()})


class FavoritesRecipes(ListView):
    template_name = 'base/favorites_recipe.html'
    context_object_name = 'revenues'

    def get_queryset(self):
        favorite_recipes = self.request.user.like.all()
        return favorite_recipes

    
    def post(self, request, *args, **kwargs):
        self.remove_recipe(request)
        return render(request, self.template_name, {'revenues': request.user.like.all()})

    
    def remove_recipe(self, request):
        values_list = list(request.POST.keys())
        id = values_list[-1]
        recipe = Revenue.objects.get(id = id)
        recipe.like.remove(request.user)


class FilterRecipes(ListView):
    template_name = 'base/filtered_recipes.html'
    model = Revenue
    context_object_name = 'recipes_local'
    paginate_by = 2
    

    def get_queryset(self):
        q = self.return_search()
        self.revenues_filter = Revenue.objects.annotate(max_date=Max('like')).filter(Q(name_revenue__icontains = q) | Q(topic__name_topic__icontains = q)).order_by('-max_date')
        return self.revenues_filter


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_recipes'] = len(self.revenues_filter)
        return context

    
    def return_search(self):
        # Pega o valor que está no atributo get do request.GET e retorna
        if self.request.GET.get('search') == None:
            q = ''
        else:
            q = self.request.GET.get('search')
        return q


class DeleteMessage(View):
    template_name = 'base/delete_message.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    
    def post(self, request, *args, **kwargs):
        message = Message.objects.get(id = kwargs['pk'])
        message.delete()
        return redirect('recipe-page', message.revenue.id)


class User(View):
    template_name = 'base/user.html'

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id = kwargs['pk'])
        p = Paginator(Revenue.objects.annotate(max_date=Max('like')).filter(host = user).order_by('max_date'), 8)
        page = request.GET.get('page')
        recipes = p.get_page(page)
        return render(request, self.template_name, {'user':user, 'recipes':recipes})


def loginUser(request):
    registration_sistem = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user == None:
            messages.error(request, 'Email ou senha inválidos')
        else:
            user.number_of_attempts = 5
            login(request, user, backend='account.backend.CustomBackend')
            return redirect('/')
    return render(request, 'base/login.html', {'registration_sistem':registration_sistem})


def logoutUser(request):
    logout(request)
    return redirect('/')