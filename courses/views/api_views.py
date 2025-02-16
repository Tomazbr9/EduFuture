from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from utils.permissions import IsInstructor, VerifyCoursePurchase
from courses.models import Course, Module, Class, Student, StudentClass, Cart
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

        # Se o instrutor for criador do curso, permite a atualização completa.
        if user == course_instructor:
            return super().partial_update(request, *args, **kwargs)
        # Caso contrário, verifica se está tentando atualizar apenas campos permitidos.
        elif any(field not in allowed_fields for field in request.data.keys()):
            # Se tentar atualizar campos não permitidos, lança um erro de permissão.
            raise PermissionDenied("Você só pode atualizar o campo permitido.")

class StudentViewSet(ModelViewSet):
    # Define o conjunto de dados padrão para a visualização.
    queryset = Student.objects.all()

    # Especifica o serializer que será usado para os objetos do modelo.
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        Sobrescreve o método get_queryset para restringir os dados exibidos.
        """
        user = self.request.user  # Obtém o usuário autenticado da requisição.
        # Filtra os objetos do queryset para incluir apenas o estudante associado ao usuário.
        return self.queryset.filter(user=user)


class StudentClassViewSet(ModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

    def partial_update(self, request, *args, **kwargs):
        # Recupera o aluno associado ao usuário autenticado.
        student = Student.objects.get(user=request.user)
        
        # Recupera a aula que está sendo atualizada.
        cls = self.get_object()

        # Verifica se a aula pertence ao aluno autenticado.
        if cls.student != student:
            raise PermissionDenied("Não é possível atualizar as aulas de outros alunos!!")
        
        # Caso a verificação seja bem-sucedida, permite a atualização parcial.
        return super().partial_update(request, *args, **kwargs)

class RegisterUserApiView(APIView):
    """
    View utilizada para fazer registros de usuários
    """

    def post(self, request) -> Response:
        # Inicializa o serializer com os dados fornecidos na requisição.
        serializer = UserRegistrationSerializer(data=request.data)

        # Verifica se os dados fornecidos são válidos.
        if serializer.is_valid():
            # Salva o novo usuário caso os dados sejam válidos.
            serializer.save()
            return Response(
                {'message': 'Usuário criado com sucesso'}, 
                status=status.HTTP_201_CREATED
            )
        
        # Retorna erros de validação caso os dados sejam inválidos.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserApiView(APIView):
    """
    View para atualizar usuários existentes
    """

    def post(self, request, pk: int) -> Response:
        # Recupera o usuário pelo ID (pk). Retorna 404 se o usuário não for encontrado.
        user = get_object_or_404(User, pk=pk)
        
        # Inicializa o serializer com o usuário encontrado e os dados fornecidos para atualização parcial.
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        
        # Verifica se os dados fornecidos são válidos.
        if serializer.is_valid():
            # Atualiza o usuário com os dados validados.
            serializer.save()
            return Response(
                {'message': 'Usuário atualizado com sucesso.'},
                status=status.HTTP_200_OK
            )
        
        # Retorna erros de validação caso os dados sejam inválidos.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    """
    View utilizada para fazer autenticação de usuários
    """

    def post(self, request):
        # Recupera o nome de usuário e a senha dos dados da requisição.
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Verifica se o nome de usuário e a senha foram fornecidos.
        if not username or not password:
            return Response(
                {'message': 'Usuário ou Senha inválidos'}, 
                status=status.HTTP_401_UNAUTHORIZED)
        
        # Autentica o usuário com as credenciais fornecidas.
        user = authenticate(username=username, password=password)

        # Retorna erro se as credenciais forem inválidas.
        if user is None:
            return Response(
                {'message': 'Credenciais inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED)
        
        # Gera um token de acesso (JWT) para o usuário autenticado.
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token) # type: ignore

        print(access_token)

        # Registra o token na sessão do usuário.
        request.session['access_token'] = access_token

        # Faz o login do usuario
        login(request, user)

        user = get_object_or_404(Student, user=request.user)
        cart, _ = Cart.objects.get_or_create(user=user)

        request.session['cart'] = cart.items

        # Retorna mensagem de sucesso no login.
        return Response(
            {
                'message': 'Login bem-sucedido!',
                'access_token': access_token,
                'refresh_token': str(refresh) 
            }
        )

        
class BuyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudentCourseSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            request.session['cart'] = {}  # Limpa o carrinho
            serializer.save()
            return Response({"message": "Cursos comprados com sucesso!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    """
    View para renovar o access_token usando o refresh_token.
    """
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'message': 'Refresh token não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response(
                {
                    'access_token': new_access_token,
                    'refresh_token': str(refresh)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': 'Refresh token inválido ou expirado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )