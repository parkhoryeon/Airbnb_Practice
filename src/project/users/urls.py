from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),                          # User 생성
    path("me", views.Me.as_view()),                           # User(Private) 조회 / User(Private) 수정
    path("change-password", views.ChangePassword.as_view()),  # 비밀번호 변경
    path("log-in", views.LogIn.as_view()),                    # 로그인
    path("log-out", views.LogOut.as_view()),                  # 로그아웃
    path("token-login", obtain_auth_token),                   # Auth Token 
    path("jwt-login", views.JWTLogIn.as_view()),                   # JWT(Json Web Token)
    path("github", views.GithubLogIn.as_view()),                   # JWT(Json Web Token)
    path("@<str:username>", views.PublicUser.as_view()),      # User(Public) 조회
]