"""
URL configuration for stocksProjectApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

from .views import custom_login, custom_logout, custom_register


app_name = "stocks"  # Esto define el namespace

urlpatterns = [
    path("", views.PortfolioView.as_view(), name="portfolio"),
    path("login/", custom_login, name="login"),
    path("logout/", custom_logout, name="logout"),
    path("register/", custom_register, name="register"),
    path("stocks/", views.CorporationListView.as_view(), name="stocks_list"),
    path("stocks/<str:ticker>/", views.CorporationDetailView.as_view(), name="detail"),
    path(
        "stocks/<str:ticker>/<int:pk>/update/",
        views.UpdateInvestmentView.as_view(),
        name="update_investment",
    ),
    path(
        "stocks/<str:ticker>/<int:pk>/delete/",
        views.DeleteInvestmentView.as_view(),
        name="delete_investment",
    ),
]
