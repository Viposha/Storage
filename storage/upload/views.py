from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, FormView
from .models import News, Files, Profile
from .forms import FilesForm, UserCreateForm, UserLoginForm, ChangeRankForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import time
from django.contrib import messages
from django.contrib.auth import login, logout
from .utils import bytes_to_mb


class AccountView(ListView):
	model = Files
	template_name = 'upload/account_list.html'
	context_object_name = 'files'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Особистий кабінет'
		return context

	def get_queryset(self):
		return Files.objects.filter(username=self.request.user.pk)

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			picked_files = request.POST.getlist('file')
			for file in picked_files:
				file_instance = Files.objects.filter(path=file, username=self.request.user.pk)
				file_instance.delete()
			return redirect(reverse('account'))


class ChangeRankView(FormView):
	form_class = ChangeRankForm

	template_name = "upload/change_rank_form.html"

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Змінити тариф'
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			form = ChangeRankForm(data=request.POST, instance=request.user)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()
				user.profile.rank = form.cleaned_data.get('rank')
				user.save()
				return redirect(reverse('home'))
			else:
				messages.error(request, 'Помилка. Перевірте дані')
		return redirect(reverse('upload'))


def register(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.rank = form.cleaned_data.get('rank')
			user.save()
			login(request, user)
			messages.success(request, 'Ви зареєструвались!')
			return redirect('upload')
		else:
			messages.error(request, 'Помилка реєстрації!')
	else:
		form = UserCreateForm()
	return render(request, 'upload/register.html', {'form': form, 'title': 'Реєстрація'})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('upload')
	else:
		form = UserLoginForm()
	return render(request, 'upload/login.html', {'form': form, 'title': 'Авторизація'})


def user_logout(request):
	logout(request)
	return redirect('login')


class ViewNews(ListView):
	model = News
	template_name = 'upload/news_list.html'
	context_object_name = 'news'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Головна'
		return context

	def get_queryset(self):
		return News.objects.all()


def model_form_upload(request):
	if request.method == 'POST':
		start = time.perf_counter()
		form = FilesForm(request.POST, request.FILES, user=request.user)
		if form.is_valid():
			file = request.FILES
			fs = FileSystemStorage()
			filename = fs.save(file["path"].name, file["path"])
			uploaded_file_url = fs.url(filename)
			size = file["path"].size
			size_Mb = bytes_to_mb(size)  # convert bytes to Mb
			name = f'{file["path"]}'
			user_id = User.objects.get(pk=request.user.pk)
			path = Files(path=name, size=size, username=user_id)
			path.save()
			end = time.perf_counter()
			result = round((end - start), 3)
			date = path.uploaded_at
			return render(request, 'upload/result.html', {'result': result, 'date': date, 'url': uploaded_file_url, 'size': size_Mb})
	else:
		form = FilesForm(user=request.user)
	return render(request, 'upload/upload.html', {'form': form, 'title': 'Завантажити'})
