from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    '''
        Creating user, saving them and returning the user
    '''

    def create_user(self, username, email, password=None, **extra_fields):

        if not username:
            raise ValueError("The username needs to be set.")

        elif not email:
            raise ValueError("The email needs to be set.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        '''
            Creating SuperUser after the user creation.
        '''
        user = self.create_user(
            username,
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True

        user.save(using=self._db)

        return user
