from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from apps.authentication.serializers import RegisterSerializer, LoginSerializer
from apps.authentication.services import create_user_service, login_user_service, refresh_token_service, google_login_service
from django.conf import settings
from decouple import config
from urllib.parse import urlencode

class RegisterView(APIView):
    def post(self, request): # rota pra registrar, vai chamar o service
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            ip = request.META.get('REMOTE_ADDR')

            result = create_user_service(
                email= serializer.validated_data['email'],
                name= serializer.validated_data['name'],
                password= serializer.validated_data['password'],
                ip=ip
            )

            response = Response({
                "refresh": result["refresh"],
            }, status=status.HTTP_201_CREATED)
    
            response.set_cookie(
                key="access_token",
                value=result["access"],
                httponly=True,
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",       
                max_age=60 * 15       
            )

            response.set_cookie(
                key="refresh_token",
                value=result["refresh"],
                httponly=True, 
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",
                max_age=60 * 60 * 24 * 30 
            )

            return response
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            ip = request.META.get('REMOTE_ADDR')

            result = login_user_service(
                email= serializer.validated_data['email'],
                password= serializer.validated_data['password'],
                ip=ip
            )

            response = Response({"message": "Login realizado com sucesso"},status=status.HTTP_200_OK)

            response.set_cookie(
                key="access_token",
                value=result["access"],
                httponly=True,
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",       
                max_age=60 * 15       
            )

            response.set_cookie(
                key="refresh_token",
                value=result["refresh"],
                httponly=True, 
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",
                max_age=60 * 60 * 24 * 30 
            )
            return response
        except AuthenticationFailed as e:
            return Response({"Não autorizado.": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token não encontrado")
        
        try:
            ip = request.META.get('REMOTE_ADDR')
            
            result = refresh_token_service(refresh=refresh_token, ip=ip);

            response = Response({"message": "Login realizado com sucesso"},status=status.HTTP_200_OK)

            response.set_cookie(
                key="access_token",
                value=result["access"],
                httponly=True,
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",       
                max_age=60 * 15       
            )

            response.set_cookie(
                key="refresh_token",
                value=result["refresh"],
                httponly=True, 
                secure=False,         # habilitar True qnd for pra deploy
                samesite="Lax",
                max_age=60 * 60 * 24 * 30 
            )
            return response
        except AuthenticationFailed as e:
            return Response({"Não autorizado.": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GoogleLoginView(APIView):
    def get(self, request):
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"

        params = {
            "client_id": config("GOOGLE_CLIENT_ID"),
            "redirect_uri": config("GOOGLE_REDIRECT_URI"),
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        url = f"{base_url}?{urlencode(params)}"
        return redirect(url)
    
class GoogleCallbackView(APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")
            ip = request.META.get('REMOTE_ADDR')

            result = google_login_service(code, ip)

            target_url = f"{config("GOOGLE_FRONTEND_URI")}/auth-callback?name={result['user'].user_id}"
            response = redirect(target_url)
            
            response.set_cookie(key="access_token", value=result["access"], httponly=True)
            response.set_cookie(key="refresh_token", value=result["refresh"], httponly=True)

            return response

        except Exception as e:
            return HttpResponse(f"Erro crítico no callback: {str(e)}", status=500)