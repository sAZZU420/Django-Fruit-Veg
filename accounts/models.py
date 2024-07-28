from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('You must give a valid email')
        if not username:
            raise ValueError('You must give a valid username')
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=300, unique=True)
    email = models.EmailField(max_length=300, unique=True)
    phone_number = models.CharField(max_length=100, null=True)

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=350, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pic", blank=True, null=True)
    cover_pic = models.ImageField(upload_to="cover_pic", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user
