from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Modelo Base para passar inforções para os demais modelos
class Base(models.Model):
    creation = models.DateTimeField(auto_now_add=True) # Data de criação
    update = models.DateTimeField(auto_now=True) # Data de atualização

    class Meta:
        abstract = True 

# Modelo Categoria, utilizado para mostrar determinado assunto desejado ao usuario
class Category(Base):
    name = models.CharField(max_length=255)

# Modelo de determina se o usario é um aluno ou instrutor
class Student(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles', default='profiles/sem_perfil.jpg')
    age = models.DateField()
    is_instructor = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

# Modelo de Endereços Multivalorado
class Address(Base):
    road = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

# Modelo de Curso 
class Course(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    objective = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    instructor = models.ForeignKey(
        Student, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

# Modelo de Modulo
class Module(Base):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'

# Modelo de Aula
class Class(models.Model):
    title = models.CharField(max_length=255)
    materials = models.FileField(upload_to='materials/', blank=True, null=True)
    module = models.ForeignKey(Module, related_name='classes', on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

# Modelo para relacionar Curso com Aluno
class StudentCourse(Base):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate = models.URLField(default="")
    completed = models.BooleanField(default=False)

# Modelo para relacionar Modulo com Aluno
class StudentModule(Base):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

# Modelo para relacionar Aula com Aluno
class StudentClass(Base):
    student = models.ForeignKey(Student, related_name='student_class', on_delete=models.CASCADE)
    cls = models.ForeignKey(Class, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class Cart(Base):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    items = models.JSONField(default=dict) 




