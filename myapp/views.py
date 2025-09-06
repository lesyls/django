from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def home_page(request):
    if request.method == 'POST':
        # Обработка формы контактов
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        service = request.POST.get('service')
        message = request.POST.get('message')

        # Здесь можно добавить отправку email или сохранение в базу
        messages.success(request, 'Ваша заявка отправлена! Мы свяжемся с вами в ближайшее время.')
        return redirect('home')

    return render(request, 'myapp/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = UserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})