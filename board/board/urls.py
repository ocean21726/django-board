"""
URL configuration for board project.

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
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from members.views import SignUpAPI, SignInAPI, register, login, NewSignUpAPI, NewSignInAPI
from boards.views import list, detail, create, update, delete

urlpatterns = [
    path('', list),
    path('admin/', admin.site.urls),
    # API 구현
    # path('api/sign-up', SignUpAPI.as_view()),
    path('api/sign-up', NewSignUpAPI.as_view()),
    # path('api/sign-in', SignInAPI.as_view()),
    path('api/sign-in', NewSignInAPI.as_view()),
    path('api/auth/refresh', TokenRefreshView.as_view()),
    # 템플릿과 연동한 구현
    path('register', register),
    path('login', login),
    path('board/list', list),
    path('board/list/<str:order_type>', list),
    path('board/detail/<int:idx>', detail),
    path('board/create', create),
    path('board/update/<int:idx>', update),
    path('board/delete/<int:idx>', delete),
]
