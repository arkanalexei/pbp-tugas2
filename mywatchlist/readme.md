 ## Jelaskan perbedaan antara JSON, XML, dan HTML!
| JSON                                              | XML                                                                     |
|---------------------------------------------------|-------------------------------------------------------------------------|
| Javascript Object Notation                        | Extensible Markup Language                                              |
| Berdasarkan bahasa pemrograman JavaScript         | Diturunkan dari SGML                                                    |
| Merupakan cara untuk merepresentasikan objek      | Bahasa markup dan menggunakan struktur tag untuk merepresentasikan data |
| Tidak support namespace                           | Support namespace                                                       |
| Support array                                     | Tidak support array                                                     |
| Lebih mudah dipahami/dibaca                       | Lebih susah dipahami/dibaca                                             |
| Tidak memakai end tag                             | Memiliki start dan end tag                                              |
| Less secured                                      | More secured                                                            |
| Tidak support komen                               | Support komen                                                           |
| Support hanya UTF-8 encoding                      | Support encoding-encoding lain                                          |
| Objek JSON memiliki tipe                          | Data XML tidak ada tipe                                                 |
| Tipe data JSON ada string, number, array, Boolean | Data XML hanya string                                                   |
| Data siap diakses sebagai objek JSON              | Data XML harus di parse dahulu                                          |
| Disupport beragam browser                         | Cross-browser parsing untuk XML bisa sedikit sulit                      |
| Mengambil value mudah                             | Mengambil value susah                                                   |
 <br>
 Sedangkan HTML sendiri merupakan standard markup language untuk web pages. Cenderung HTML dibantu dengan teknologi seperti CSS atau JavaScript. Cara kerjanya adalah web browser akan menerima dokumen HTML dari server atau local storange dan render halam tersebut. HTML mendeskripsikan struktur sebuah web page secara semantik. Elemen elemen dalam HTML itu diberi tags seperti p atau h1. HTML itu cenderung lebih mudah dipelajari. Perbedaannya dengan JSON adalah JSON lebih cenderung digunakan untuk data storage dan transfer. Namun JSON lebih rumit dari HTML. Dengan HTML kita bisa membuat static page. Sedangkan dengan XML itu dinamis. Design goal dari XML berpatok pada simplisitas, generalitas, dan kegunaannya dalam internet. Untuk perbedaan lebih lengkap silahkan simak tabel berikut.

 <br>
 
| HTML                              | XML                                 |
|-----------------------------------|-------------------------------------|
| Hyper Text Markup Language        | Extensible Markup Language          |
| Static                            | Dinamis                             |
| Mampu mengabaikan error kecil     | Tidak mampu mengabaikan error kecil |
| Case insensitive                  | Case sensitive                      |
| Predefined tags                   | User defined tags                   |
| Tidak membawa data, hanya display | Membawa data dari dan ke database   |
| Ukuran file cenderung rendah      | Ukurang file cenderung besar        |
| Dibutuhkan closing tags           | Tidak dibutuhkan closing tags       |
| Tidak preserve white space        | Preserve white space                |
 
 ## Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
 Misalnya kita ingin membangun suatu platform dimana kita harus mengirim data dari suatu stack ke stck lainnya. Tentunya data-data tersebut memiliki berbagai macam bentuk seperti HTML, XML, JSON, dan lain-lain. Jadi agar proses tersebut lancar, diperlukan data delivery.
 
 
 ## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
 ### Membuat aplikasi baru
 ```py
 django-admin startapp mywatchlist
```
### Menambahkan path mywatchlist
Pada urls.py di project_django, tambahkan
```py
path('mywatchlist/', include('mywatchlist.urls')),
```
dan jangan lupa masukkan mywatchlist di installed apps.
### Membuat model MyWatchList dengan beberapa tribut
Pada models.py di folder app mywatchlist, tambahkan
```py
class MyWatchList(models.Model):
    watched = models.BooleanField()
    title = models.TextField()
    rating = models.IntegerField()
    release_date = models.TextField()
    review = models.TextField()
```
### Mengisi 10 data
Membuat initial_movie_data.json dengan format sebagai berikut
```json
[
    {
        "model": "mywatchlist.mywatchlist",
        "pk": 1,
        "fields": {    
            "watched": true,
            "title": "Interstellar",
            "rating": 4,
            "release_date": "2014-10-06",
            "review": "Mankind was born on Earth. It was never meant to die here."

        }
    }
  ]
  ```
  Dan selanjutnya untuk 10 data lain
  ### Membuat routing html, xml, json
  Pada urls.py mywatchlist, 
  ```py
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>', show_json_by_id, name='show_json_by_id'),
    path('xml/<int:id>', show_xml_by_id, name='show_json_by_id'),
    path('html/', show_mywatchlist, name='show_mywatchlist'),
```
Jangan lupa definisikan fungsi fungsi tersebut di views.py sebagai berikut
```py
def show_xml(request):
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = MyWatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = MyWatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")   
```
### Deployment ke Heroku
Proses ini sama persis seperti di tutorial. Pertama kita harus membuat app baru di Heroku. Lalu menambahkan secret yakni Heroku app name dan api key di secret repo kita. Lalu tinggal deploy deh!

## POSTMAN
