from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView, DetailView
from .models import Corporation, Investment, Usuario
from .forms import InvestmentForm
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from django.urls import reverse_lazy
from django.views.generic import FormView

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Investment, Usuario
from .forms import InvestmentForm
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from .forms import UpdateInvestmentForm


class CorporationListView(TemplateView):
    template_name = "stocks/index.html"
    context_object_name = "corporations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["corporations"] = Corporation.objects.all()
        return context


class CorporationDetailView(DetailView):
    model = Corporation
    template_name = "stocks/detail.html"
    context_object_name = "corporation"
    slug_field = "ticker"  # Indica que el identificador es el campo "ticker"
    slug_url_kwarg = "ticker"  # Hace que la URL use "ticker" en vez de "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["investment_list"] = Investment.objects.filter(corporation=self.object)
        return context


class PortfolioView(TemplateView):
    """
    Vista protegida: solo accesible si el usuario está autenticado.
    """

    template_name = "investments/index.html"

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:  # Verifica si el usuario está autenticado
            return redirect("stocks:login")  # Redirige al login si no está autenticado

        # 🔹 Recupera el usuario y lo asigna a request.user para evitar problemas posteriores
        request.user = get_object_or_404(Usuario, id=user_id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InvestmentForm()
        context["investments"] = Investment.objects.filter(user=self.request.user)

        user_id = self.request.session.get("user_id")

        if user_id:
            usuario = get_object_or_404(Usuario, id=user_id)
            context["usuario"] = usuario
        return context

    def post(self, request, *args, **kwargs):
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)

            # 🔹 Obtener el usuario de la sesión
            user_id = request.session.get("user_id")
            if not user_id:
                return redirect("stocks:login")  # Si no hay usuario en sesión, redirige

            # 🔹 Obtener el usuario correspondiente en `Usuario`
            usuario = get_object_or_404(Usuario, id=user_id)

            # Asignar el usuario autenticado al investment
            investment.user = usuario
            investment.save()
            return redirect("stocks:portfolio")

        return self.render_to_response(self.get_context_data(form=form))


class UpdateInvestmentView(UpdateView):
    model = Investment
    form_class = UpdateInvestmentForm
    template_name = "investments/update_investment.html"
    success_url = reverse_lazy("stocks:portfolio")

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.session.get("user_id")
        return queryset.filter(user_id=user_id) if user_id else queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["investment"] = self.object
        return context


class DeleteInvestmentView(DeleteView):
    model = Investment
    success_url = reverse_lazy("stocks:portfolio")

    def get_queryset(self):
        queryset = super().get_queryset()  # Obtiene todas las inversiones
        user_id = self.request.session.get("user_id")  # Obtiene el usuario de la sesión
        return queryset.filter(user_id=user_id) if user_id else queryset.none()


def login_required(view_func):
    """
    Decorador para restringir el acceso a usuarios no autenticados.
    Redirige a la página de login si el usuario no ha iniciado sesión.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("login")  # Redirige al login si no está autenticado
        return view_func(request, *args, **kwargs)

    return wrapper


def custom_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get(
            "username_or_email"
        )  # 🔹 Campo para nombre de usuario o email
        password = request.POST.get("password")

        try:
            # Intenta buscar al usuario por nombre de usuario
            user = Usuario.objects.get(username=username_or_email)
        except Usuario.DoesNotExist:
            try:
                # Si no se encuentra por nombre de usuario, busca por email
                user = Usuario.objects.get(email=username_or_email)
            except Usuario.DoesNotExist:
                # Si no se encuentra por ninguno, muestra un error
                return render(
                    request,
                    "investments/login.html",
                    {"error": "Usuario no encontrado"},
                )

        # Verifica la contraseña
        if user.check_password(password):
            # Almacena el ID del usuario en la sesión
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("stocks:portfolio")  # 🔹 Redirige al portfolio
        else:
            # Contraseña incorrecta
            return render(
                request,
                "investments/login.html",
                {"error": "Contraseña incorrecta"},
            )
    else:
        return render(request, "investments/login.html")


def custom_logout(request):
    request.session.flush()
    return redirect("stocks:login")


def custom_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)  # 👈 ¡Agregado request.FILES!
        if form.is_valid():
            user = form.save()  # 🔹 Guarda el usuario con la contraseña encriptada
            return redirect(
                "stocks:portfolio"
            )  # 🔹 Redirige al usuario a la página principal
    else:
        form = RegisterForm()

    return render(request, "investments/register.html", {"form": form})
