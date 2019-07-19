from django.conf.urls import include
from django.urls import path, re_path
# from django.conf import settings
# from django.conf.urls.static import static
import django.contrib.auth.views

from . import views


urlpatterns = [
    path(r"", views.homepage, name="homepage"),
    re_path(r"^contact/$", views.contact_admins, name="contact_admins"),
    re_path(
        r"^admin/$", views.django_admin_page, name="django_admin_page"
    ),  # link to admin
    re_path(r"^accounts/", include("registration.backends.default.urls")),
    # names = 'auth_login' /login 'auth_logout' 'registration_register' 'auth_password_reset' 'registration_activate'
    re_path(r"accounts/register/$", views.register, name="register"),
    re_path(r"accounts/login/$", django.contrib.auth.views.LoginView, name="login"),
    re_path(
        r"accounts/logout/$",
        django.contrib.auth.views.LogoutView,
        name="logout",
        kwargs={"next_page": "/"},
    ),
    re_path(r"^test/$", views.GeneratePdf.as_view(), name="test"),
    re_path(r"^invoice/$", views.GenerateInvoice.as_view(), name="invoice"),
    re_path(r"^contactjn/$", views.contact_jinja, name="contact_jinja"),
]