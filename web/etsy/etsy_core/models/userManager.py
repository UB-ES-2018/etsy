from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, image=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            profile_image = image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def update_name(self, first_name, last_name, id):
        # Update user's first name and last name
        user = User.objects.filter(id = id)
        fname = User.objects.filter(first_name=first_name)
        lname = User.objects.filter(last_name=last_name)
        if fname.exists() and lname.exists():
        	return "Username already exists."
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
