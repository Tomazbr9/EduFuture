from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from utils.permissions import IsInstructor, VerifyCoursePurchase
from courses.models import Course, Module, Class, Student, StudentClass
from courses.serializers import (
    CourseSerializer, ModuleSerializer, ClassSerializer, 
    UserRegistrationSerializer, StudentSerializer, 
    StudentCourseSerializer, StudentClassSerializer, UserUpdateSerializer
)

class CourseViewSet(ModelViewSet):
    # Define o conjunto de consultas padrão para os cursos.
    queryset = Course.objects.all()
    
    # Especifica o serializer a ser utilizado para serializar os objetos do modelo.
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Define as permissões com base na ação realizada.
        """
        if self.action in ['list', 'retrieve']:
            # Permite acesso irrestrito para visualizar a lista de cursos ou detalhes individuais.
            permission_classes = [AllowAny]
        else:
            # Restringe ações como criação, atualização e exclusão a instrutores.
            permission_classes = [IsInstructor]
        
        # Instancia e retorna as permissões configuradas.
        return [permission() for permission in permission_classes]

            
class ModuleViewSet(ModelViewSet):
    # Define o conjunto de consultas padrão para os módulos.
    queryset = Module.objects.all()
    
    # Especifica o serializer a ser utilizado para serializar os objetos do modelo.
    serializer_class = ModuleSerializer

    def get_permissions(self):
        """
        Define as permissões com base na ação realizada.
        """
        if self.action in ['list', 'retrieve']:
            # Permite acesso irrestrito para visualizar a lista de módulos ou detalhes individuais.
            permission_classes = [AllowAny]
        else:
            # Restringe ações como criação, atualização e exclusão a instrutores.
            permission_classes = [IsInstructor]
        
        # Instancia e retorna as permissões configuradas.
        return [permission() for permission in permission_classes]



class ClassViewSet(ModelViewSet):
    # Define o conjunto de consultas padrão para as aulas.
    queryset = Class.objects.all()

    # Especifica o serializer a ser utilizado para serializar os objetos do modelo.
    serializer_class = ClassSerializer

    def get_permissions(self):
        """
        Define as permissões com base na ação realizada.
        """
        # Restringe o acesso para verificar se o usuário comprou o curso ou se ele é o instrutor da classe.
        permission_classes = [VerifyCoursePurchase]     
        return [permission() for permission in permission_classes]
    
    def partial_update(self, request, *args, **kwargs):
        """
        Permite a atualização parcial de uma aula, mas com restrições específicas.
        """
        allowed_fields = ['completed']  # Define que apenas o campo 'completed' pode ser atualizado.

        
        user = Student.objects.get(user=request.user)
        
        # Obtém o instrutor associado à aula (o instrutor do curso do módulo).
        course_instructor = self.get_object().module.course.instructor

        # verificar isso aqui amanhã

        # Se o instrutor for criador do curso, permite a atualização completa.
        if user == course_instructor:
            return super().partial_update(request, *args, **kwargs)
        # Caso contrário, verifica se está tentando atualizar apenas campos permitidos.
        elif any(field not in allowed_fields for field in request.data.keys()):
            # Se tentar atualizar campos não permitidos, lança um erro de permissão.
            raise PermissionDenied("Você só pode atualizar o campo permitido.")

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



        


