from django.urls import path,re_path
from .views import (
    account_home_view,
)

urlpatterns = [
    path('',account_home_view,name="home"),
   
]