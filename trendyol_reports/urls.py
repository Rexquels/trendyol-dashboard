from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "rapor/yeni/",
        views.create_report,
        name="create_report"
    ),

]