from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import News, Files
from .forms import FilesForm, UserCreateForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import time
from django.contrib import messages


def register(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.rank = form.cleaned_data.get('rank')
			user.save()
			messages.success(request, 'Ви зареєструвались!')
			return redirect('login')
		else:
			messages.error(request, 'Помилка реєстрації!')
	else:
		form = UserCreateForm()
	return render(request, 'upload/register.html', {'form': form})


def login(request):
	return render(request, 'upload/login.html')


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
		form = FilesForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES
			fs = FileSystemStorage()
			filename = fs.save(file["path"].name, file["path"])
			uploaded_file_url = fs.url(filename)
			size = file["path"].size
			name = f'paths/{file["path"]}'
			user_id = User.objects.get(pk=request.user.pk)
			path = Files(path=name, size=size, username=user_id)
			path.save()
			end = time.perf_counter()
			result = round((end - start), 3)
			date = path.uploaded_at
			return render(request, 'upload/result.html', {'result': result, 'date': date, 'url': uploaded_file_url})
	else:
		form = FilesForm()
	return render(request, 'upload/upload.html', {'form': form})