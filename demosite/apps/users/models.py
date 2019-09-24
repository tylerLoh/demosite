from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	"""
	AbstractUser
	(id, password, last_login, first_name, last_name,
	username, email, is_superuser, is_staff, date_joined, is_active)
	"""
	nick_name = models.CharField(max_length=30, default="")
	gender = models.CharField(
		choices=(("male", "Male"),("female", "Female")),
		default="male",
		max_length=6
	)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		# set is active to true first, since have no email activation
		if not self.is_active:
			self.is_active = True

	def __str__(self):
		return self.username