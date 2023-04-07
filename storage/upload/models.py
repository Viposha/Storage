from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	Junior = 'Jr'
	Middle = 'Ml'
	Senior = 'Sr'
	RANKS = [
		(Junior, 'Junior'),
		(Middle, 'Middle'),
		(Senior, 'Senior')
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rank = models.CharField(max_length=2, choices=RANKS, default='Tr')

	def __str__(self):
		return self.rank


class Files(models.Model):
	path = models.FileField(upload_to='files/')
	size = models.IntegerField(blank=False)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	username = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name='user')

	def __str__(self):
		return 'self.path'

	class Meta:
		verbose_name = 'Файл'
		verbose_name_plural = 'Файли'
		ordering = ['size']


class News(models.Model):
	title = models.CharField(max_length=100, primary_key=True)
	content = models.TextField()
	photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Новина'
		verbose_name_plural = 'Новини'

