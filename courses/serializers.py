from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Course, Module, Class, Student, Instructor, Category, StudentCourse
)

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = [
            'name',
            'description',
            'price',
            'image',
            'student',
            'instructor'
        ]

    def create(self, validated_data) -> Course:
        user = self.context['request'].user
        instructor = Instructor.objects.get(user=user)
        
        return Course.objects.create(instructor=instructor, **validated_data)

class ModuleSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Module
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):

    courses = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    
    class Meta:
        model = Instructor
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
            raise serializers.ValidationError('Estudante não existe!')
    
    def validate(self, data):
        
        course = data['course']
        student = self.get_authenticated_student()

        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Este curso ja foi comprado!")
        return data
    
    def create(self, validated_data) -> StudentCourse:
        student = self.get_authenticated_student()
        return StudentCourse.objects.create(student=student, **validated_data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    is_instructor = serializers.BooleanField(write_only=True, required=True)
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

            if is_instructor:
                Instructor.objects.create(
                    user=user,
                    age=age,
                    description=description,
                    category=category
                )
            else:
                Student.objects.create(
                    user=user,
                    age=age,
                    category=category
                )
            
        return user

    
