from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in
from web3 import Web3
# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self,phonenumber,password,is_active=True,is_staff=False,is_admin=False):
		if not phonenumber:
			raise ValueError("User must have a Phone Number")
		if not password:
			raise ValueError("User must have a Password")

		user_obj=self.model(
			phonenumber=phonenumber,
		)
		user_obj.set_password(password)
		user_obj.set_admin(is_admin)
		user_obj.set_staff(is_staff)
		user_obj.set_is_active(is_active)
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self,phonenumber,password):
		user=self.create_user(
            phonenumber,
            password=password,
            is_active=True,
            is_staff=True,
        )
		return user

	def create_superuser(self,phonenumber,password):
		user=self.create_user(
            phonenumber,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
        )
		return user

class MyUser(AbstractBaseUser):
	fullname=models.CharField(max_length=120)
	address_line_1=models.CharField(max_length=120)
	address_line_2=models.CharField(max_length=120,blank=True,null=True)
	city=models.CharField(max_length=50)
	state=models.CharField(max_length=50)
	pincode=models.IntegerField(null=True,blank=True)
	phonenumber=PhoneNumberField(unique=True)
	active=models.BooleanField(default=True)
	staff=models.BooleanField(default=False)
	admin=models.BooleanField(default=False)
	user_hash=models.CharField(max_length=200,blank=True,null=True)

	USERNAME_FIELD='phonenumber'
	#REQUIRED_FIELDS=[fullname,address_line_1,city,state,pincode,phonenumber]

	objects=UserManager()
	
	def __str__(self):
		return str(self.phonenumber)

	def get_full_name(self):
		return str(self.fullname)

	def get_short_name(self):
		return str(self.fullname)

	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,perm,obj=None):
		return True

	def set_admin(self,is_admin):
		self.admin=is_admin

	def set_staff(self,is_staff):
		self.staff=is_staff

	def set_is_active(self,is_activated):
		self.active=is_activated

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active


def set_hash(sender,user,request,**kwargs):
	w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
	account=w3.eth.accounts[user.id - 1]
	user.user_hash=account
	user.save()

user_logged_in.connect(set_hash)