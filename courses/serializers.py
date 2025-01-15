from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Course, Module, Class, Student, Category, 
    StudentCourse, StudentModule, StudentClass
)

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        # Define o modelo e os campos que serão serializados.
        model = Course
        fields = [
            'name',          # Nome do curso.
            'description',   # Descrição do curso.
            'price',         # Preço do curso.
            'image',         # Imagem representativa do curso.
            'instructor'     # Instrutor responsável pelo curso.
        ]

    def create(self, validated_data) -> Course:
        """
        Cria um curso e associa o instrutor autenticado como responsável.
        """
        # Recupera o usuário autenticado através do contexto da requisição.
        user = self.context['request'].user
        
        # Obtém a instância do instrutor associada ao usuário autenticado.
        instructor = Student.objects.get(user=user)

        # Cria o curso com os dados validados, associando-o ao instrutor autenticado.
        return Course.objects.create(instructor=instructor, **validated_data)


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        # Define o modelo associado ao serializer.
        model = Module
        # Inclui todos os campos do modelo.
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Cria um novo módulo e associa automaticamente a todos os estudantes inscritos no curso.
        """
        course = validated_data['course']  # Obtém o curso associado ao novo módulo.

        # Recupera o instrutor autenticado com base na requisição.
        instructor = Student.objects.get(user=self.context['request'].user)

        # Verifica se o instrutor autenticado é o mesmo responsável pelo curso.
        if course.instructor != instructor:
            raise serializers.ValidationError(
                "Não é possível criar módulos em cursos de outros professores."
            )

        # Chama o método `create` da classe pai para criar o novo módulo.
        new_module = super().create(validated_data)

        # Obtém o curso associado ao novo módulo (refatoração para reutilização).
        course = new_module.course

        # Recupera a lista de IDs dos estudantes matriculados no curso.
        student_list = StudentCourse.objects.filter(
            course=course
        ).values_list('student', flat=True)
        
        # Itera sobre os IDs dos estudantes para associá-los ao novo módulo.
        for student_id in student_list:
            student = Student.objects.get(pk=student_id)
            # Cria ou recupera a relação entre o estudante e o módulo.
            StudentModule.objects.get_or_create(
                module=new_module, student=student
            )
        
        # Retorna o novo módulo criado.
        return new_module


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        # Define o modelo associado ao serializer.
        model = Class
        # Inclui todos os campos do modelo.
        fields = '__all__'

    def create(self, validated_data):
        """
        Cria uma nova aula e associa automaticamente a todos os estudantes inscritos no curso.
        """
        module = validated_data['module']  # Obtém o módulo associado à nova aula.

        # Recupera o instrutor autenticado com base na requisição.
        instructor = Student.objects.get(user=self.context['request'].user)

        # Verifica se o instrutor autenticado é o mesmo responsável pelo curso.
        if module.course.instructor != instructor:
            raise serializers.ValidationError(
                "Não é possível criar aulas em cursos de outros professores."
            )

        # Chama o método `create` da classe pai para criar a nova aula.
        new_class = super().create(validated_data)

        # Obtém o curso associado ao módulo da nova aula.
        course = new_class.module.course

        # Recupera a lista de IDs dos estudantes matriculados no curso.
        student_list = StudentCourse.objects.filter(
            course=course
        ).values_list('student', flat=True)

        # Itera sobre os IDs dos estudantes para associá-los à nova aula.
        for student_id in student_list:
            student = Student.objects.get(pk=student_id)
            # Cria ou recupera a relação entre o estudante e a nova aula.
            StudentClass.objects.get_or_create(
                cls=new_class, student=student
            )

        # Retorna a nova aula criada.
        return new_class



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'

class StudentCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Define o modelo associado ao serializer.
        model = StudentCourse
        
        # Especifica os campos manipulados pelo serializer.
        fields = [
            'student',
            'course',
        ]
        
        # Define o campo 'student' como somente leitura.
        read_only_fields = ['student']
    
    def get_authenticated_student(self):
        """
        Recupera o estudante autenticado com base no usuário da requisição.
        """
        user = self.context['request'].user  # Obtém o usuário autenticado da requisição.
        
        try:
            # Recupera o objeto Student associado ao usuário autenticado.
            return Student.objects.get(user=user)
        except Student.DoesNotExist:
            # Lança um erro caso o usuário autenticado não esteja vinculado a um estudante.
            raise serializers.ValidationError('Aluno não existe!')
    
    def validate(self, data):
        """
        Valida se o estudante já comprou o curso.
        """
        course = data['course']  # Recupera o curso enviado nos dados.
        student = self.get_authenticated_student()  # Recupera o estudante autenticado.

        # Verifica se o curso já foi comprado pelo estudante.
        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Este curso já foi comprado!")
        
        return data  # Retorna os dados validados.
    
    def create(self, validated_data):
        """
        Cria a relação entre estudante e curso, incluindo os módulos e aulas.
        """
        student = self.get_authenticated_student()  # Recupera o estudante autenticado.
        course = validated_data.get('course')  # Obtém o curso dos dados validados.
        
        with transaction.atomic():
            # Cria ou recupera a relação entre o estudante e cada módulo do curso.
            for module in course.modules.all():  # type: ignore
                StudentModule.objects.get_or_create(
                    student=student, module=module
                )
            
            # Cria ou recupera a relação entre o estudante e cada aula de cada módulo.
            for module in course.modules.all():  # type: ignore
                for cls in module.classes.all():
                    StudentClass.objects.get_or_create(
                        student=student, cls=cls
                    )

            # Cria ou recupera a relação entre o estudante e o curso.
            student_course, _ = StudentCourse.objects.get_or_create(
                student=student, course=course
            )
            return student_course  # Retorna o objeto criado.

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Define se o usuário será instrutor, com padrão como falso.
    is_instructor = serializers.BooleanField(default=False)
    
    # Campo opcional para descrição do usuário, somente para escrita.
    description = serializers.CharField(
        max_length=255, required=False, write_only=True
    )
    
    # Relaciona o usuário a uma categoria específica. Este campo é obrigatório e somente para escrita.
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, required=True
    )
    
    # Campo obrigatório para a data de nascimento, somente para escrita.
    age = serializers.DateField(write_only=True, required=True)

    class Meta:
        # Define o modelo associado ao serializer.
        model = User
        # Especifica os campos manipulados pelo serializer.
        fields = [
            'id', 
            'username',
            'email',
            'password', 
            'first_name',
            'last_name', 
            'age',
            'is_instructor',
            'category',
            'description',
        ]
        # Torna o campo de senha somente para escrita.
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        # Valida se o nome de usuário já está em uso.
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Já Existe um usuário com este nome'
            )
        return value
    
    def validate_email(self, value):
        # Valida se o email já está em uso.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Já existe um usuário com este email.'
            )
        return value
    
    def validate(self, attrs):
        # Valida se o nome de usuário e a senha são iguais.
        if attrs['username'] == attrs['password']:
            raise serializers.ValidationError(
                'Usuário e senha não podem serem iguais.'
            )
        return attrs
    
    def create(self, validated_data) -> User:
        # Extração de dados do usuário para criação.
        is_instructor = validated_data.get('is_instructor')
        category = validated_data.get('category')
        description = validated_data.get('description')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        age = validated_data['age']

        # Garantia de atomicidade durante a criação dos registros.
        with transaction.atomic():
            # Criação do objeto User com dados validados.
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=first_name,
                last_name=last_name
            )
  
            # Criação do objeto Student associado ao User.
            Student.objects.create(
                user=user,
                is_instructor=is_instructor,
                age=age,
                description=description,
                category=category,
            )
            
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    # Campo opcional para a data de nascimento ou idade, pode ser útil para validação ou cálculo.
    age = serializers.DateField(required=False)
    
    # Define se o usuário é um instrutor, com valor padrão como falso.
    is_instructor = serializers.BooleanField(default=False)
    
    # Campo para uma descrição curta, que pode ser opcional e aceita valores vazios.
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    
    # Relaciona o usuário a uma categoria, opcional e aceita valores nulos.
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        # Define o modelo associado a este serializer.
        model = User
        # Especifica os campos que podem ser atualizados.
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'is_instructor',
            'description',
            'category',
        ]
        # Adiciona regras extras para tornar certos campos opcionais.
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        # Separa os dados relacionados ao modelo User.
        user_data = {key: validated_data.pop(key) for key in [
            'username', 'email', 'first_name', 'last_name'
        ] if key in validated_data}

        # Atualiza cada atributo do modelo User com os valores fornecidos.
        for attr, value in user_data.items():
            setattr(instance, attr, value)

        # Os dados restantes são tratados como pertencentes ao modelo Student.
        student_data = validated_data
        # Obtém ou cria uma instância de Student associada ao usuário.
        student, _ = Student.objects.get_or_create(user=instance)
        # Atualiza os atributos do Student com os valores fornecidos.
        for attr, value in student_data.items():
            setattr(student, attr, value)

        # Salva as mudanças nos objetos User e Student.
        instance.save()
        student.save()
        return instance
