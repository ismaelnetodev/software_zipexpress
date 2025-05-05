from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class CustomUsuarioManager(UserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O email não foi informado.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")
        
        return self._create_user(email, password, **extra_fields)
        
        
class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField("Email", unique=True)
    nome = models.CharField("Nome", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    NIVEL_ACESSOS_CHOICES = (
        ("admin", "Admin"),
        ("compras", "Compras"),
        ("operador", "Operador"),
    )
    nivel_acesso = models.CharField(
        "Nível de acesso", choices=NIVEL_ACESSOS_CHOICES, max_length=20
    )
    is_active = models.BooleanField("Ativo", default=True)
    is_staff = models.BooleanField("Acesso ao admin", default=False)

    last_login = models.DateTimeField("Último login", blank=True, null=True)

    objects = CustomUsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "cargo", "nivel_acesso"]  # ajuste conforme desejar

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"