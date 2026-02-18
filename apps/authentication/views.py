from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.authentication.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer
from apps.authentication.services import create_user_service

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
                "user": {
                    "user_id": result["user"],
                    "email": result["user"],
                    "name": result["user"]
                }
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
