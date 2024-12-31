from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Base(models.Model):
    creation = models.DateTimeField(auto_now_add=True) # Data de criação
    update = models.DateTimeField(auto_now=True) # Data de atualização

    class Meta:
        abstract = True 

class Category(Base):
    name = models.CharField(max_length=255)

class Student(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.DateField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField('Course', through='StudentCourse')

class Instructor(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.DateField()
    description = models.TextField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

class Address(Base):
    road = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

class Course(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    image = models.ImageField(upload_to='courses', blank=True, null=True)
    completed = models.BooleanField(default=False)
    registered = models.IntegerField(default=0)
    instructor = models.ForeignKey(
        Instructor, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Module(Base):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'

class Class(models.Model):
    title = models.CharField(max_length=255)
    materials = models.FileField(upload_to='materials', blank=True, null=True)
    completed = models.BooleanField(default=False)
    module = models.ForeignKey(Module, related_name='classes', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

class StudentCourse(Base):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


