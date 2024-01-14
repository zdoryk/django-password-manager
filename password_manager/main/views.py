from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PasswordEntry
from .forms import PasswordEntryForm
from .utils import get_encryption_key, encrypt, decrypt
from .signals import synchronize_data
from datetime import datetime


def index(request):
    passwords = PasswordEntry.objects.filter(is_deleted=False)
    key = get_encryption_key()
    for password in passwords:
        password.password = decrypt(password.password, key).strip(' ')
    return render(request, 'index.html', {'passwords': passwords})


def create_password(request):
    key = get_encryption_key()
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']

            encrypted_password = encrypt(password, key).decode("utf-8", "ignore")
            password_entry = PasswordEntry.objects.create(service=service, login=login, password=encrypted_password)
            messages.success(request, f"Password for {password_entry.login} created successfully!")
            return redirect('index')
    else:
        form = PasswordEntryForm()

    return render(request, 'create_password.html', {'form': form})


def delete_password(request, id):
    password_entry = PasswordEntry.objects.get(id=id)
    if request.method == 'POST':
        password_entry.is_deleted = True
        password_entry.deleted_at = datetime.now()
        password_entry.save()
        return redirect('index')
    return render(request, 'delete.html')


def sync(request):
    synchronize_data(None)
    return redirect('index')
