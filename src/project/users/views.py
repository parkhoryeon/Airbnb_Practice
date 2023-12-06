import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from . import serializers
from .models import User
import requests

from django.db.utils import IntegrityError


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class Users(APIView):

    def post(self, request):
        serializer = serializers.PrivateUserSerializer(data=request.data)
        password = request.data.get("password")
        if not password:
            raise ParseError
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # 그냥 user.pasword를 하면 안된다. 무조건 set_password()를 해줘야 한다.
            user.save()  
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class PublicUser(APIView):

    def get(self, request, username):   
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    

class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user 
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError
        

class LogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome"})
        else:
            return Response({"error": "Wrong password"})
        

class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})
    

class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # 토큰에 서명
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256",)
            return Response({"token": token})
        else:
            return Response({"error": "Wrong Password"})
        

class GithubLogIn(APIView):

    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id=0d95a90665671ebe5f20&client_secret={settings.GH_SECRET}", headers={
                "Accept": "application/json"
            })
            # print("⭐ : ", access_token.json())
            access_token = access_token.json().get("access_token")
            # print("⭐ : ", access_token)
            user_data = requests.get(
                "https://api.github.com/user", 
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                },
            )
            print('⭐ : ', user_data.json())
            user_data = user_data.json()
            
            user_emails = requests.get(
                "https://api.github.com/user/emails", 
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                },
            )
            print('⭐ : ', user_emails.json())
            user_emails = user_emails.json()
            try:
                print("🚫1")
                user = User.objects.get(email=user_emails[0]['email'])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                print("🚫2")
                try:
                    user = User.objects.create(
                        username=user_data.get('login'),
                        email=user_emails[0]['email'],
                        name=user_data.get('name'),
                        avatar=user_data.get("avatar_url"),
                    )
                    print("🚫USER : ", user)
                    user.set_unusable_password()
                    user.save()
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                except IntegrityError as e:
                    # 에러 발생 시 예외를 캐치하고 에러 메시지 출력
                    print(f"❌❌❌Error creating user: {e}")
        except Exception:
            print("❌")
            return Response(status=status.HTTP_400_BAD_REQUEST)