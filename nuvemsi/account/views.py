from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import KeyUser
import secrets 


# Create your views here.

#Kullanıcı login girişini sağladığımız fonksiyon.
def login_request(request):
    #Kullanıcı giriş yapmışsa login sayfasına erişemesin
    if request.user.is_active:
        return redirect("home")

    if request.method == "POST":
        #form ekranından verileri alıyoruz.
        username= request.POST["username"]
        password= request.POST["password"]
    
    #Veritabanı ile eşitleyerek kontrol sağlıyoruz
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request,"account/login.html",{
                "error":"Mail adresi ya da parola yanlış."
            })
    return render(request,"account/login.html")

#Kullanıcı kaydını yaptığımız fonksiyon.
def register_request(request):
    # #Kullanıcı giriş yapmışsa register sayfasına erişemesin
    if request.user.is_active:
        return redirect("home")

    if request.method == "POST":
        #form ekranından verileri alıyoruz.
        username= request.POST["username"]
        firstname= request.POST["firstname"]
        lastname= request.POST["lastname"]
        email= request.POST["email"]
        phone= request.POST["phone"]
        password= request.POST["password"]
        repassword= request.POST["repassword"]
    
    #Oluşturulan parolaların birbirinin aynısı olup olmadığını kontrol ediyoruz
        if password == repassword:
            #Daha önce user kullanıcı adında kayıt var mı kontrol ediyoruz.
            if User.objects.filter(username=username).exists():
                #Hata mesajını döndürüyoruz.
                return render(request, "account/register.html",
                    {
                        #Oluşan hatadan dolayı sayfa içerisinde girilen bilgileri sayfaya tekrr post ederek aynı bilgilerin girilmesini önlüyoruz.
                        "error":"Bu kullanıcı adında oluşturulan bir kayıt var.",
                        "username":username,
                        "firstname":firstname,
                        "lastname":lastname,
                        "email":email,
                        "phone":phone
                    }
                )
            #Daha önce mail ve telefon numaraları ile oluşturulan kayıt var mı kontrol sağlıyoruz.
            elif User.objects.filter(email=email).exists():
                return render(request, "account/register.html",
                    {
                        #Oluşan hatadan dolayı sayfa içerisinde girilen bilgileri sayfaya tekrr post ederek aynı bilgilerin girilmesini önlüyoruz.
                        "error":"Bu mail için oluşturulan bir kayıt var.",
                        "username":username,
                        "firstname":firstname,
                        "lastname":lastname,
                        "email":email,
                        "phone":phone
                    }
                )

            elif KeyUser.objects.filter(phone=phone).exists():
                return render(request, "account/register.html", 
                    {
                        #Oluşan hatadan dolayı sayfa içerisinde girilen bilgileri sayfaya tekrr post ederek aynı bilgilerin girilmesini önlüyoruz.
                        "error":"Bu telefon numarası için oluşturulan bir kayıt var.",
                        "username":username,
                        "firstname":firstname,
                        "lastname":lastname,
                        "email":email,
                        "phone":phone
                    }
                )
            #Kullanıcı kaydını yapıyoruz.
            else:
                user=User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email,password=password)
                kuser=KeyUser.objects.create(user_name=username, phone=phone, key=keymake())
                kuser.save()
                user.save()
                return redirect("login")
        else:
            return render(request, "account/register.html", 
                {
                    #Oluşan hatadan dolayı sayfa içerisinde girilen bilgileri sayfaya tekrr post ederek aynı bilgilerin girilmesini önlüyoruz.
                    "error":"Parola eşleşmiyor.",
                    "username":username,
                    "firstname":firstname,
                    "lastname":lastname,
                    "email":email,
                    "phone":phone
                }
            )
            
    return render(request, "account/register.html")
#Kullanıcı çıkış işlemini gerçekleştirdiğimiz fonksiyon.
def logout_request(request):
    #logout hazır fonksiyonunu kullanarak çıkış işlemini gerçekleştiriyoruz.
    logout(request)
    return redirect("login")

#Anahtar üreteci
def keymake():
    return secrets.token_hex(nbytes=16)
    