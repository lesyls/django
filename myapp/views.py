from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm, ContactForm, UserProfileForm, ReviewForm
from .models import ContactRequest, UserProfile, Review


def home_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            if request.user.is_authenticated:
                contact_request.email = request.user.email
            contact_request.save()

            messages.success(request, 'Заявка отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('profile')  # Редирект на профиль вместо home
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()

    return render(request, 'myapp/home.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Получаем историю заявок пользователя
    contact_requests = ContactRequest.objects.filter(
        email=request.user.email
    ).order_by('-created_at')

    context = {
        'form': form,
        'profile': user_profile,
        'contact_requests': contact_requests
    }

    return render(request, 'myapp/profile.html', context)


def reviews_view(request):
    approved_reviews = Review.objects.filter(status='approved').order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Для добавления отзыва необходимо авторизоваться.')
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв отправлен на модерацию! После проверки он появится на сайте.')
            return redirect('reviews')
    else:
        form = ReviewForm()

    context = {
        'reviews': approved_reviews,
        'form': form,
        'user_review_exists': Review.objects.filter(
            user=request.user).exists() if request.user.is_authenticated else False
    }
    return render(request, 'myapp/reviews.html', context)


def home_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            if request.user.is_authenticated:
                contact_request.email = request.user.email
            contact_request.save()
            messages.success(request, 'Заявка отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()

    # Получаем 3 последних одобренных отзыва для главной страницы
    latest_reviews = Review.objects.filter(status='approved').order_by('-created_at')[:3]

    return render(request, 'myapp/home.html', {
        'form': form,
        'latest_reviews': latest_reviews
    })