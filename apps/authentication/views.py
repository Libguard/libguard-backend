from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.authentication.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer
from apps.authentication.services import create_user_service, login_user_service

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

            return Response({
                "refresh": result["refresh"],
                "access": result["access"],
                "user": result["user"]
            }, status=status.HTTP_201_CREATED)
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

            return Response({
                "refresh": result["refresh"],
                "access": result["access"],
                "user": result["user"]
            }, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"Não autorizado.": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
