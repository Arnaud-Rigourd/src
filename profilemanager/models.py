from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class Profile(models.Model):
    """
    Profile model represents the extended User model to provide more detailed information about the user WHEN its category is 'developpeur'. This is a one-to-one relation with the User model.

    Fields:
    - id: A unique identifier for the profile.
    - description: A textual description of the user's profile.
    - job: The job type of the user, can be either 'front-end', 'back-end' or 'full-stack'.
    - visible: A boolean value indicating whether the profile is visible to others or not.
    - user: A one-to-one link to the user this profile belongs to.
    """
    JOBS_CHOICES = (
        ('front-end', 'Front-end'),
        ('back-end', 'Back-end'),
        ('full-stack', 'Full-stack'),
    )

    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    job = models.CharField(
        max_length=250,
        choices=JOBS_CHOICES,
        blank=False)
    visible = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Stacks(models.Model):
    """
    Stacks model represents the different technologies the user is comfortable with.

    Fields:
    - id: A unique identifier for the stack.
    - name: The name of the technology.
    - profile: A foreign key linking to the profile to which this stack belongs.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Projects(models.Model):
    """
    Projects model represents the different projects a user has worked on.

    Fields:
    - id: A unique identifier for the project.
    - name: The name of the project.
    - description: A textual description of the project.
    - used_stacks: A text field describing the stacks used in the project.
    - link: A link to the project, if it's hosted somewhere.
    - profile: A foreign key linking to the profile to which this project belongs.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)
    used_stacks = models.ManyToManyField(Stacks)
    # used_stacks = models.TextField(blank=True)
    link = models.URLField(blank=True, default="")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Company(models.Model):
    """
    Company model represents the company for which a user works WHEN its category is 'company'.

    Fields:
    - name: The name of the company.
    - user: A one-to-one link to the user to which this company belongs.
    """

    name = models.CharField(max_length=250, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the default save method to automatically fill in the company's name with the name from the associated user's company_name attribute.
        """
        self.name = self.user.company_name
        super().save(*args, **kwargs)
