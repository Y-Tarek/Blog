from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from shared.utility import CsrfTokenMixin


from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(APIView):
    """ Register API """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    """ Login API """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=username, password=password)
            if user:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
              return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(CsrfTokenMixin,APIView):
    permission_classes = [IsAuthenticated]
    """ Logout API """
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)