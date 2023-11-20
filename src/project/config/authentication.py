import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class TrustMeBroAuthentication(BaseAuthentication):

    # Override
    """ 
    커스텀 인증 
    가장 멍청한 방법. 이렇게 하면 안된다.
    user를 찾아서 그 user를 반환한다.
    만약 없다면 None을 반환하면 된다. 
    """
    def authenticate(self, request):
        username = request.headers.get('Trust-Me')
        if not username:
            return None 
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
             raise AuthenticationFailed(f'No user {username}')
        

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # print('⭐ : ', request.headers)
        token = request.headers.get('Jwt')
        # print('⭐ TOKEN : ', token)
        if not token:
            return None
        # print('⭐ SECRET_KEY : ', settings.SECRET_KEY)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        # print('⭐ DECODED : ', decoded)
        pk = decoded.get('pk')
        # print('⭐ PK : ', pk)
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            # print('⭐ USER : ', user)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")