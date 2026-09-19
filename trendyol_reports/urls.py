from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Yeni haftalık rapor
    path(
        "rapor/yeni/",
        views.create_report,
        name="create_report"
    ),

    # Giriş
    path(
        "giris/",
        auth_views.LoginView.as_view(
            template_name="trendyol_reports/login.html"
        ),
        name="login"
    ),

    # Çıkış
    path(
        "cikis/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

]