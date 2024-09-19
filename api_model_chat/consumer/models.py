import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class BaseModelQuerySet(models.QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now(), is_active=False)

class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True, is_active=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    deleted_at = models.DateTimeField('Deleted At', null=True, blank=True)
    is_active = models.BooleanField('Is Active', default=True)

    objects = BaseManager()

    def soft_delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)

    def recover(self):
        self.deleted_at = None
        self.is_active = True
        self.save()

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True')

        return self._create_user(email, password, **extra_fields)
    
# Classe Usuário
class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]

    code = models.UUIDField("Código uuid4", default=uuid.uuid4, editable=False)
    matricula = models.IntegerField('Matrícula', unique=True, null=True, blank=True)
    name = models.CharField('Name', max_length=255, unique=True)
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    photo = models.ImageField('Photo', upload_to='img_profile', null=True, blank=True)
    email = models.EmailField('Email', unique=True, null=True, blank=True)
    is_staff = models.BooleanField('Is Staff', default=False)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.name