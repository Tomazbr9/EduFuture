from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Course, Module, Class, Student, Category, 
    StudentCourse, StudentModule, StudentClass
)

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = [
            'name',
            'description',
            'price',
            'image',
            'instructor'
        ]

    def create(self, validated_data) -> Course:
        user = self.context['request'].user
        instructor = Student.objects.get(user=user)
        
        return Course.objects.create(instructor=instructor, **validated_data)

class ModuleSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Module
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

    def create(self, validated_name):
        ...

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
        model = StudentCourse

        fields = [
            'student',
            'course',
            
        ]

        read_only_fields = ['student']
    
    def get_authenticated_student(self):
        """
        Recupera usuário authenticado
        """
        user = self.context['request'].user
        
        try:
            return Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise serializers.ValidationError('Aluno não existe!')
    
    def validate(self, data):
        
        course = data['course']
        student = self.get_authenticated_student()

        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Este curso ja foi comprado!")
        return data
    
    def create(self, validated_data):
        student = self.get_authenticated_student()
        course = validated_data.get('course')
        
        with transaction.atomic():

            for module in course.modules.all(): #type: ignore
                StudentModule.objects.get_or_create(
                    student=student, module=module)
            
            for module in course.modules.all(): #type: ignore
                for cls in module.classes.all():
                    StudentClass.objects.get_or_create(student=student, cls=cls)

            return StudentCourse.objects.get_or_create(student=student, course=course)
            
class UserRegistrationSerializer(serializers.ModelSerializer):
    
    is_instructor = serializers.BooleanField(default=False)
    description = serializers.CharField(
        max_length=255, required=False, write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, required=True
    )
    age = serializers.DateField(write_only=True, required=True)

    class Meta:
        model = User
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
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Já Existe um usuário com este nome'
            )
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Já existe um usuário com este email.'
            )
        return value
    
    def validate(self, attrs):
        if attrs['username'] == attrs['password']:
            raise serializers.ValidationError(
                'Usuário e senha não podem serem iguais.'
            )
        
        return attrs
    
    def create(self, validated_data) -> User:
        is_instructor = validated_data.get('is_instructor')
        category = validated_data.get('category')
        description = validated_data.get('description')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        age = validated_data['age']

        with transaction.atomic():

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=first_name,
                last_name=last_name
            )
  
            Student.objects.create(
                user=user,
                is_instructor=is_instructor,
                age=age,
                description=description,
                category=category,
            )
            
        return user

    
