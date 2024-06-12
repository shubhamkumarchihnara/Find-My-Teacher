from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("resetPassword",views.resetPassword,name="resetPassword"),
    path("logout",views.logout,name="logout"),
    path("search",views.search,name="search"),
    path("MakeAppointment",views.MakeAppointment,name="MakeAppointment"),
]
