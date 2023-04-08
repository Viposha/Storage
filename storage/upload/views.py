from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import News, Files, Profile
from .forms import FilesForm, UserCreateForm, UserLoginForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import time
from django.contrib import messages
from django.contrib.auth import login, logout
from .utils import bytes_to_mb


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
	return render(request, 'upload/register.html', {'form': form})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('upload')
	else:
		form = UserLoginForm()
	return render(request, 'upload/login.html', {'form': form})


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
	return render(request, 'upload/upload.html', {'form': form})