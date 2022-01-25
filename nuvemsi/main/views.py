from django.http.response import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from account.models import KeyUser
from main.models import Uploadİmg, UploadDoc
import base64, os
from django.core.files.storage import FileSystemStorage
from Crypto.Cipher import AES



# Create your views here.
 
    
def home(request):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    context={

           "liste":Uploadİmg.objects.filter(username=request.user.username, userid=request.user.id)
        
    }
    
    
    return render(request,"main/index.html",context)


#Resim yükleme işleminin gerçekleştiği fonksiyon
def uploadimg(request):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    #Butona tıklandığında yapılacak işlemler
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']#Resim dosyasının seçilmesi
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)#Resim Dosyasının yüklenmesi
        size=int(os.path.getsize(".//uploads/"+upload.name)/1024) #Resim boyutunu aldığımız kısım
        #Bu kısımda yüklediğimiz resim dosyasının yolunu bularak base64'e çeviriyoruz.
        #Böylece veri tabanına base64 ile string bir değer kaydediyoruz.
        with open(".//uploads/"+upload.name, "rb") as imagescalculate:
            base64codeimg = base64.b64encode(imagescalculate.read()).decode("utf-8")   
        os.remove(".//uploads/"+upload.name)
        #Tabloları birleştirme işlemi için kullandığımız sorgumuz. Anahtar id sini aldık.
        keyid= KeyUser.objects.get(user_name=request.user.username)  
        # key=keyid.key  
        # vi=key[:16] 
        # aes = AES.new(key.encode("utf8"), AES.MODE_CBC, vi.encode("utf8"))
        # encd = aes.encrypt(base64codeimg) 
        #veri=base64codeimg[2:-1] 
        #Veritabanına kayıt işlemini gerçekleştiriyoruz     
        imgUpload=Uploadİmg.objects.create(size=size, imgcode=base64codeimg, username=request.user.username, userid=request.user.id, keyid=keyid.id, imgname=upload.name)
        imgUpload.save()
        return  render(request, "main/uploadimg.html",
            {
                #Kullanıcı resim dosyası seçmediğinde hata versin.
                "success":"Yükleme işlemi başarılı.",
            })
 
    return  render(request, "main/uploadimg.html")



def uploaddoc(request):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    #Butona tıklandığında yapılacak işlemler
   
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']#Dosya dosyasının seçilmesi
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)#Dosya Dosyasının yüklenmesi
        size=int(os.path.getsize(".//uploads/"+upload.name)/1024) #Dosya boyutunu aldığımız kısım
        #Bu kısımda yüklediğimiz dosya dosyasının yolunu bularak base64'e çeviriyoruz.
        #Böylece veri tabanına base64 ile string bir değer kaydediyoruz.
        with open(".//uploads/"+upload.name, "rb") as pdfFile:
            text = base64.b64encode(pdfFile.read()).decode("utf-8")  
        os.remove(".//uploads/"+upload.name)
        #Tabloları birleştirme işlemi için kullandığımız sorgumuz. Anahtar id sini aldık.
        keyid= KeyUser.objects.get(user_name=request.user.username) 
        # key=keyid.key  
        # vi=key[:16] 
        # aes = AES.new(key.encode("utf8"), AES.MODE_CBC, vi.encode("utf8"))
        # encd = aes.encrypt(text) 
        #veri=text[2:-1]       
        #Veritabanına kayıt işlemini gerçekleştiriyoruz     
        uploadDoc=UploadDoc.objects.create(size=size, docname=upload.name, username=request.user.username, userid=request.user.id, keyid=keyid.id, doccode=text)
        uploadDoc.save()
        return  render(request, "main/uploaddoc.html",
            {
                #Kullanıcı resim dosyası seçmediğinde hata versin.
                "success":"Yükleme işlemi başarılı.",
            })
    return  render(request, "main/uploaddoc.html")
        


#Çıkış yapmak için kullanılan fonksiyon
def logout_request(request):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    #logout hazır fonksiyonunu kullanarak çıkış işlemini gerçekleştiriyoruz.
    logout(request)
    return redirect("login")


#Verilerin silme işlemini gerçekleştirdiğimiz fonksiyonumuz
def delete_request(request, pk):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    obj = get_object_or_404(Uploadİmg, id = pk)
    obj.delete()
    return render(request, "main/index.html")


#Kayıtlı verilerimizi indirmek için kullandığımız fonksiyonumuz.
def download_request(request, pk):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    file = Uploadİmg.objects.get(id=pk)
    filename = file.imgname
    filecode= file.imgcode
    decodeit = open('.//uploads/'+str(filename), 'wb')
    decodeit.write(base64.b64decode((filecode)))
    decodeit.close()
    filelocal = './/uploads/'+str(filename)
    
    file_path = os.path.join(filelocal)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response 
    #Note: uploads klasörünün içini temizleme(download fonksiyonu !!!)
    return render(request, "main/index.html")


def doclist_request(request):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    context={

           "liste":UploadDoc.objects.filter(username=request.user.username, userid=request.user.id)
    }
    return render(request,"main/doclist.html",context)

#Doküman indirme işlemini gerçekleştirdiğimiz bölüm.
def docdown_request(request, pk):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    file = UploadDoc.objects.get(id=pk)
    filename = file.docname
    filecode= file.doccode
    decodeit = open('.//uploads/'+str(filename), 'wb')
    decodeit.write(base64.b64decode((filecode)))
    decodeit.close()
    filelocal = './/uploads/'+str(filename)
    file_path = os.path.join(filelocal)
    return FileResponse(open(file_path , 'rb'), as_attachment=True, content_type='application/pdf')


#Veritabanından döküman sildiğimiz fonksiyon.
def deldoc_request(request, pk):
    #Kullanıcı giriş yapmadan sayfalara erişim sağlayamasın. 
    if request.user.is_active == False:
        return redirect("login")
    obj = get_object_or_404(UploadDoc, id = pk)
    obj.delete()
    return render(request, "main/index.html")