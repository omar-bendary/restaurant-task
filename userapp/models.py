from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, employee_number, password=None, **extra_fields):
        if not employee_number:
            raise ValueError('The Employee Number must be set')
        user = self.model(employee_number=employee_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(employee_number, password, **extra_fields)


class UserRoleChoices(models.TextChoices):
    EMPLOYEE = ('EMPLOYEE', 'Employee')
    ADMIN = ('ADMIN', 'Admin')


class User(AbstractBaseUser, PermissionsMixin):
    employee_number = models.CharField(max_length=4, unique=True,  validators=[
                                       RegexValidator(r'^\d{4}$', 'Employee number must be 4 digits.')],)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=8, choices=UserRoleChoices.choices, default=UserRoleChoices.EMPLOYEE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(6)]
    )
    objects = UserManager()

    USERNAME_FIELD = 'employee_number'

    def __str__(self):
        return self.name
