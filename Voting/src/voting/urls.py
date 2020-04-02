"""voting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from .views import index
from accounts.views import register_page,login_page
from vote.views import userHome
from parties.views import partyInfo
from vote.views import castVote,voteSuccess,verifyVote
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path('',index,name="index"),
	path('register',register_page,name="register"),
	path('login',login_page,name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('home',userHome,name="userHome"),
    path('party-information',partyInfo,name="partyInfo"),
    path('vote',castVote,name="castVote"),
    path('vote-successful',voteSuccess,name="voteSuccess"),
    path('verify-vote',verifyVote,name="verifyVote"),
    path('account/',include(("accounts.urls","accounts"),namespace="account")),
    path('admin/', admin.site.urls),
]
