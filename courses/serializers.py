from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Course, Module, Class, Student, Instructor, Category

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = '__all__'

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
    class Meta:
        model = Instructor
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    is_instructor = serializers.BooleanField(write_only=True, required=True)
    description = serializers.CharField(
        max_length=255, required=False, write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, required=True
    )

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'password', 
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
                'Já existe um usuário com este email'
            )
        return value
    
    def create(self, validated_data) -> User:

        validated_data['password'] = make_password(validated_data['password'])

        is_instructor = validated_data.get('is_instructor')
        category = validated_data.get('category')
        description = validated_data.get('description')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        if is_instructor:
            Instructor.objects.create(
                user=user,
                description=description,
                category=category
            )
        else:
            Student.objects.create(
                user=user,
                category=category
            )
        
        return user

    
