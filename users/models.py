from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


roles = (("admin", "admin"), ("user", "user"))


# this will allow to create superusers based on our given models
class UserAccountManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name="",
        last_name="",
        phone_no="",
        password=None,
    ):

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        first_name="",
        last_name="",
        phone_no="",
        password=None,
    ):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            password=password,
        )
        print(user)

        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user


# Create your models here.
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    phone_no = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(
        upload_to="users_profile_pictures/",
        default="users_profile_pictures/profile.png",
        null=True,
        blank=True,
    )
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(
        max_length=255, null=True, blank=True, default="Pakistan"
    )
    about = models.TextField(max_length=1024, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=12, null=False, blank=False, choices=roles, default="admin"
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.first_name + " " + self.last_name
