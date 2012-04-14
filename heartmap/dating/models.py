from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	GENDER_CHOICES = (
		(u'M', u'Male'),
		(u'F', u'Female'),
		(u'B', u'Both'),
	)

	birthday = models.DateField(blank = True, null = True)
	gender = models.CharField(max_length = 2, choices=GENDER_CHOICES, blank = True, null = True)
	seeking = models.CharField(max_length = 2, choices=GENDER_CHOICES, blank = True, null = True)
	phone = models.CharField(max_length = 12, blank = True, null = True)
	summary = models.TextField(blank = True, null = True)
	photo = models.FileField(upload_to = "profiles", blank = True, null = True)
	address = models.CharField(max_length = 100, blank = True, null = True)
	city = models.CharField(max_length = 52, blank = True, null = True)
	province = models.CharField(max_length = 52, blank = True, null = True)
	postal = models.CharField(max_length = 52, blank = True, null = True)

	def get_age(self):
		today = date.today()

		try: # raised when birth date is February 29 and the current year is not a leap year
			birthday = self.birthday.replace(year=today.year)
		except ValueError:
			birthday = self.birthday.replace(year=today.year, day=self.birthday.day-1)
		
		if birthday > today:
			return today.year - self.birthday.year - 1
		else:
			return today.year - self.birthday.year


class Calls(models.Model):
	caller = models.ForeignKey(User, related_name = "callers")
	callee = models.ForeignKey(User, related_name = "callees")
	allowed = models.BooleanField(default = True)

class Gift(models.Model):
	image = models.URLField(blank = True)

class Received(models.Model):
	sender = models.ForeignKey(User, related_name = "senders")
	receiver = models.ForeignKey(User, related_name = "receivers")
	gift = models.ForeignKey(Gift, related_name = "gifts")

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User) 