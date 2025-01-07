from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from utils.permissions import IsInstructor, VerifyCoursePurchase
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Course, Module, Class, Student, StudentClass
from .serializers import (
    CourseSerializer, ModuleSerializer, ClassSerializer, 
    UserRegistrationSerializer, StudentSerializer, 
    StudentCourseSerializer, StudentClassSerializer, UserUpdateSerializer
)

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsInstructor]
        
        return [permission() for permission in permission_classes]
        
            
class ModuleViewSet(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsInstructor]
        
        return [permission() for permission in permission_classes]


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_permissions(self): 
        permission_classes = [VerifyCoursePurchase]     
        return [permission() for permission in permission_classes]
    
    def partial_update(self, request, *args, **kwargs):
        allowed_fields = ['completed']

        if any(field not in allowed_fields for field in request.data.keys()):
            raise PermissionDenied("Você só pode atualizar o campo permitido.")
        
        return super().partial_update(request, *args, **kwargs)

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

class StudentClassViewSet(ModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

class RegisterUserApiView(APIView):
    """
    View utilizada para fazer registros de usuarios
    """

    def post(self, request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Usuário criado com sucesso'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserApiView(APIView):
    """
    View para atualizar usuários existentes
    """

    def patch(self, request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Usuário atualizado com sucesso.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(APIView):
    """
    View utilizada para fazer autenticação de usuários
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'message': 'Usuário ou Senha inválidos'}, 
                status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'detail': 'Credenciais inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED)
        
        reflesh = RefreshToken.for_user(user)
        access_token = str(reflesh.access_token) # type: ignore

        print(access_token)

        request.session['access_token'] = access_token

        return Response(
            {'message': 'login bem-sucedido!'}
        )
        
class BuyApiView(APIView):
    """
    API View Utilizada para vincular aluno e curso 
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudentCourseSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        


