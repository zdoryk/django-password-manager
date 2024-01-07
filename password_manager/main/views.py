from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PasswordEntry
from keyring import get_password
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

key = get_password('pm_v1', 'sk')


def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))


def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    decrypted_data = cipher.decrypt(enc)
    return decrypted_data.decode('utf-8')


def index(request):
    passwords = PasswordEntry.objects.all()
    for password in passwords:
        password.password = decrypt(password.password).strip(' ')
    return render(request, 'index.html', {'passwords': passwords})


def create_password(request):
    if request.method == 'POST':
        # Retrieve data from the form
        print(request.POST)
        service = request.POST.get('service')
        login = request.POST.get('login')
        password = request.POST.get('password')

        # Encrypt the password using passlib's CryptContext
        # TODO: add encryption
        encrypted_password = encrypt(password).decode("utf-8", "ignore")

        # Create a new PasswordEntry record
        password_entry = PasswordEntry.objects.create(service=service, login=login, password=encrypted_password)

        # For demonstration purposes, let's display a success message
        messages.success(request, f"Password for {password_entry.login} created successfully!")

    return redirect('index')


def delete_password(request, id):
    password_entry = PasswordEntry.objects.get(id=id)
    if request.method == 'POST':
        password_entry.delete()
        return redirect('/')
    return render(request, 'delete.html')
