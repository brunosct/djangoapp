from django import forms
from .models import Corporation, Investment, Usuario
from django.contrib.auth.hashers import make_password


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["corporation", "stocks_amount", "price_at_purchase"]
        labels = {
            "corporation": "Compañía",
            "stocks_amount": "Cantidad de acciones",
            "price_at_purchase": "Precio de compra",
        }
        widgets = {
            "corporation": forms.Select(attrs={"class": "form-control"}),
            "stocks_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "price_at_purchase": forms.NumberInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "corporation": {
                "required": "Este campo es obligatorio",
            },
            "stocks_amount": {
                "required": "Este campo es obligatorio",
            },
            "price_at_purchase": {
                "required": "Este campo es obligatorio",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["corporation"].empty_label = "Seleccione una compañía"


class UpdateInvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = [
            "stocks_amount",
            "price_at_purchase",
        ]  # Campos que el usuario puede actualizar
        labels = {
            "stocks_amount": "Cantidad de Acciones",
            "price_at_purchase": "Precio de Compra",
        }
        widgets = {
            "stocks_amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "price_at_purchase": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }
        error_messages = {
            "stocks_amount": {
                "required": "Este campo es obligatorio",
            },
            "price_at_purchase": {
                "required": "Este campo es obligatorio",
            },
        }


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nombre de usuario o correo electrónico",
        error_messages={"required": "Este campo es obligatorio"},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Contraseña",
        error_messages={"required": "Este campo es obligatorio"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username_or_email"].label = (
            "Nombre de usuario o correo electrónico"
        )
        self.fields["password"].label = "Contraseña"


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nombre",
        error_messages={"required": "Este campo es obligatorio"},
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Correo electrónico",
        error_messages={"required": "Este campo es obligatorio"},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Contraseña",
        error_messages={"required": "Este campo es obligatorio"},
    )
    logo = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="Logo",
        required=False,
    )

    class Meta:
        model = Usuario
        fields = ["username", "email", "password", "logo"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # 🔹 Encripta la contraseña
        if commit:
            user.save()
        return user
